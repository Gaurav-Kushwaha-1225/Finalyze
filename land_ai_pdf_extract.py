from pathlib import Path
from landingai_ade import LandingAIADE

client = LandingAIADE()
response = client.parse(document=Path("amazon.pdf"))
Path("amazon.md").write_text(response.markdown)
print("✅ Done! Check output.md")
