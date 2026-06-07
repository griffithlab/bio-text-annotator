from collections import defaultdict


def _aggregate_flat(entities: list[dict], source_id: str) -> dict:
    grouped = defaultdict(lambda: {
        "count": 0,
        "mentions": []
    })

    for entity in entities:
        key = (entity["type"], entity["text"])

        grouped[key]["count"] += 1

        mention = {
            "text": entity["text"],
            "start": entity.get("start"),
            "end": entity.get("end"),
        }

        if "subtype" in entity:
            mention["subtype"] = entity["subtype"]

        if "normalized_id" in entity:
            mention["normalized_id"] = entity["normalized_id"]

        grouped[key]["mentions"].append(mention)

    aggregated_entities = [
        {
            "type": etype,
            "text": etext,
            "count": data["count"],
            "mentions": data["mentions"]
        }
        for (etype, etext), data in sorted(grouped.items())
    ]

    return {
        "source_id": source_id,
        "total_entities": len(entities),
        "unique_entities": len(aggregated_entities),
        "entities": aggregated_entities
    }

def _aggregate_by_document(documents: list[dict], source_id: str) -> dict:
    output_docs = []

    total_entities = 0
    global_keys = set()

    for doc in documents:
        grouped = defaultdict(lambda: {
            "count": 0,
            "mentions": []
        })

        for entity in doc["entities"]:
            key = (entity["type"], entity["text"])

            grouped[key]["count"] += 1
            total_entities += 1
            global_keys.add(key)

            mention = {
                "text": entity["text"],
                "start": entity.get("start"),
                "end": entity.get("end"),
            }

            if "subtype" in entity:
                mention["subtype"] = entity["subtype"]

            if "normalized_id" in entity:
                mention["normalized_id"] = entity["normalized_id"]

            grouped[key]["mentions"].append(mention)

        aggregated = [
            {
                "type": etype,
                "text": etext,
                "count": data["count"],
                "mentions": data["mentions"]
            }
            for (etype, etext), data in sorted(grouped.items())
        ]

        output_docs.append({
            "doc_id": doc["doc_id"],
            "total_entities": len(doc["entities"]),
            "unique_entities": len(aggregated),
            "entities": aggregated
        })

    return {
        "source_id": source_id,
        "total_entities": total_entities,
        "unique_entities": len(global_keys),
        "documents": output_docs
    }

def aggregate_entities(
    documents: list[dict],
    source_id: str,
    output_mode: str = "document"
) -> dict:

    if output_mode == "flat":
        all_entities = []
        for doc in documents:
            all_entities.extend(doc["entities"])
        return _aggregate_flat(all_entities, source_id)

    return _aggregate_by_document(documents, source_id)