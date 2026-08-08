import logging

logger = logging.getLogger(__name__)

# Sigma field name -> normalized event key
FIELD_MAP = {
    "image": "process_name",
    "parentimage": "parent_process",
    "commandline": "command_line",
    "parentcommandline": "parent_command_line",
    "targetobject": "target_object",
    "targetimage": "target_image",
    "targetfilename": "target_filename",
    "destinationip": "dest_ip",
    "destinationport": "dest_port",
    "queryname": "query_name",
    "user": "user",
    "sourceimage": "source_image",
}


class SigmaEngine:
    def __init__(self, rules):
        self.rules = rules
        logger.info(f"SigmaEngine initialized with {len(rules)} rules.")

    def _match_condition(self, field_name, condition, event_value):
        if not event_value:
            return False

        event_value = str(event_value).lower()

        modifier = None
        if '|' in field_name:
            _, modifier = field_name.split('|', 1)
            modifier = modifier.lower()

        conditions = condition if isinstance(condition, list) else [condition]
        conditions = [str(c).lower() for c in conditions]

        if modifier == 'endswith':
            return any(event_value.endswith(c) for c in conditions)
        elif modifier == 'startswith':
            return any(event_value.startswith(c) for c in conditions)
        elif modifier == 'contains':
            return any(c in event_value for c in conditions)
        elif modifier == 'contains|all' or modifier == 'all':
            return all(c in event_value for c in conditions)
        else:
            return any(event_value == c for c in conditions)

    def _match_block(self, block, event):
        """AND logic across fields within one selection/filter block."""
        for field, condition in block.items():
            base_field = field.split('|')[0].lower()
            event_field = FIELD_MAP.get(base_field, base_field)
            event_val = event.get(event_field)
            if not self._match_condition(field, condition, event_val):
                return False
        return True

    def _evaluate_condition(self, condition_str, detection, event):
        """
        Minimal boolean condition evaluator supporting:
        'x', 'x and y', 'x or y', 'x and not y'
        Sufficient for majority of single-line Sigma conditions.
        Does not support 1/all of selection* wildcard syntax.
        """
        condition_str = condition_str.strip()
        tokens = condition_str.split()

        # Build a dict of block_name -> bool result, evaluated lazily
        block_names = [k for k in detection.keys() if k != 'condition']
        results = {}
        for name in block_names:
            block = detection[name]
            if isinstance(block, dict):
                results[name] = self._match_block(block, event)
            elif isinstance(block, list):
                # list of blocks = OR across sub-blocks
                results[name] = any(self._match_block(b, event) for b in block if isinstance(b, dict))
            else:
                results[name] = False

        # Very small expression evaluator: replace names with True/False, then eval safely
        expr = condition_str
        for name in sorted(results.keys(), key=len, reverse=True):
            expr = expr.replace(name, str(results[name]))
        expr = expr.replace(" and ", " and ").replace(" or ", " or ").replace(" not ", " not ")

        try:
            # Only allow and/or/not/True/False tokens through
            allowed = {"and", "or", "not", "True", "False", "(", ")"}
            safe_tokens = [t for t in expr.replace("(", " ( ").replace(")", " ) ").split()]
            if all(t in allowed for t in safe_tokens):
                return eval(expr)
        except Exception as e:
            logger.error(f"Condition eval failed for '{condition_str}': {e}")

        # Fallback: if condition just references a single block name directly
        return results.get(condition_str, False)

    def match_event(self, event):
        matches = []
        for rule in self.rules:
            try:
                detection = rule.get('detection', {})
                condition_str = detection.get('condition', '')

                if not condition_str:
                    continue

                is_match = self._evaluate_condition(condition_str, detection, event)

                if is_match:
                    technique_id = None
                    for tag in rule.get('tags', []):
                        if tag.startswith('attack.t'):
                            technique_id = tag.replace('attack.', '').upper()
                            break

                    matches.append({
                        "rule_name": rule.get('title', 'Unknown Rule'),
                        "severity": rule.get('level', 'Medium').capitalize(),
                        "technique_id": technique_id
                    })
            except Exception as e:
                logger.error(f"Error evaluating rule {rule.get('title')}: {e}")

        return matches