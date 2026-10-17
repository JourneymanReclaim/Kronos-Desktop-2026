from pathlib import Path
from collections import Counter


class FileManager:
    def __init__(self, directory="."):
        self.directory = Path(directory)

    def scan(self):
        return [path for path in self.directory.rglob("*") if path.is_file()]

    def statistics(self):
        files = self.scan()
        extensions = Counter(
            path.suffix.lower() or "[no extension]"
            for path in files
        )

        total_size = sum(path.stat().st_size for path in files)

        return files, extensions, total_size

    def search(self, query):
        query = query.lower()

        return [
            path for path in self.scan()
            if query in path.name.lower()
        ]

    def report(self):
        files, extensions, total_size = self.statistics()

        print("File Manager")
        print("============")
        print(f"Directory: {self.directory.resolve()}")
        print(f"Files: {len(files)}")
        print(f"Total size: {total_size / 1024:.2f} KB")

        print("\nFile Types")
        print("----------")

        for extension, count in extensions.most_common():
            print(f"{extension}: {count}")

        print("\nLargest Files")
        print("-------------")

        for path in sorted(
            files,
            key=lambda item: item.stat().st_size,
            reverse=True
        )[:5]:
            size = path.stat().st_size / 1024
            print(f"{path} | {size:.2f} KB")


manager = FileManager(".")

manager.report()

print("\nSearch Results")
print("--------------")

for file in manager.search("python"):
    print(file)