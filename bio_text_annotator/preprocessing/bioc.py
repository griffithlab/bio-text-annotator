from xml.sax.saxutils import escape


def text_to_bioc(text: str, document_id: str = "document") -> str:
    text = escape(text)

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<collection>
  <document>
    <id>{document_id}</id>
    <passage>
      <offset>0</offset>
      <text>{text}</text>
    </passage>
  </document>
</collection>
"""