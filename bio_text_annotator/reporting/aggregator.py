from collections import defaultdict


def aggregate_entities(
    entities: list[dict],
    source_id: str
) -> dict:

    grouped = defaultdict(lambda: {
        "count": 0,
        "mentions": []
    })

    for entity in entities:
        key = (
            entity["type"],
            entity["text"]
        )

        grouped[key]["count"] += 1

        mention = {
            "text": entity["text"],
            "start": entity.get("start"),
            "end": entity.get("end"),
        }

        # preserve optional fields
        if "subtype" in entity:
            mention["subtype"] = entity["subtype"]

        if "normalized_id" in entity:
            mention["normalized_id"] = entity["normalized_id"]

        grouped[key]["mentions"].append(mention)

    aggregated_entities = []

    for (entity_type, entity_text), data in sorted(grouped.items()):
        aggregated_entities.append({
            "type": entity_type,
            "text": entity_text,
            "count": data["count"],
            "mentions": data["mentions"]
        })

    return {
        "source_id": source_id,
        "total_entities": len(entities),
        "unique_entities": len(aggregated_entities),
        "entities": aggregated_entities
    }