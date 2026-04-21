# debug.py
import chromadb

client = chromadb.Client()
collection = client.get_collection("notes")

print(f"Count: {collection.count()}")

items = collection.get(limit=3)
print("Keys:", list(items.keys()))
print("Has documents:", len(items.get("documents", [])) > 0 if items.get("documents") else False)

if items.get("documents"):
    print("First doc:", items["documents"][0][:200] if items["documents"] else "No docs")
    if items.get("metadatas"):
        print("First metadata:", items["metadatas"][0])