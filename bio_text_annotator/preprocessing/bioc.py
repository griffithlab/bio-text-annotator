from xml.sax.saxutils import escape


def text_to_bioc(
    text: str,
    document_id: str = "document"
) -> str:

    text = escape(text)

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<collection>
  <source>PubMed</source>
  <date>20260607</date>
  <key>tmVar</key>

  <document>
    <id>{document_id}</id>

    <passage>
      <infon key="type">abstract</infon>
      <infon key="section">ABSTRACT</infon>
      <offset>0</offset>
      <text>{text}</text>
    </passage>

  </document>
</collection>
"""