from collections import defaultdict


def aggregate_entities(
    entities: list[dict],
    source_id: str
) -> dict:
    """
    Aggregate extracted entities into a report structure.

    Args:
        entities: List of extracted entity dictionaries.
        source_id: Identifier for the processed source.

    Returns:
        Aggregated report dictionary.
    """

    counts = defaultdict(int)

    for entity in entities:
        key = (
            entity["type"],
            entity["text"]
        )

        counts[key] += 1

    aggregated_entities = []

    for (entity_type, entity_text), count in sorted(counts.items()):
        aggregated_entities.append({
            "type": entity_type,
            "text": entity_text,
            "count": count
        })

    report = {
        "source_id": source_id,
        "total_entities": len(entities),
        "unique_entities": len(aggregated_entities),
        "entities": aggregated_entities
    }

    return report