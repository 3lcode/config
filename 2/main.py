import argparse
import os
import subprocess
from datetime import datetime

def parse_arguments():
    parser = argparse.ArgumentParser(description="Dependency Graph Visualizer")
    parser.add_argument("--graphviz_path", required=True, help="Path to the graph visualization program")
    parser.add_argument("--repo_path", required=True, help="Path to the Git repository")
    parser.add_argument("--output_path", required=True, help="Path to save the dependency graph image")
    parser.add_argument("--since_date", required=True, help="Filter commits after this date (YYYY-MM-DD)")
    return parser.parse_args()

def get_git_commits(repo_path, since_date):
    since_date = datetime.strptime(since_date, "%Y-%m-%d").isoformat()
    cmd = ["git", "log", "--since", since_date, "--pretty=format:%H"]
    result = subprocess.run(cmd, cwd=repo_path, capture_output=True, text=True, check=True)
    return result.stdout.splitlines()

def get_commit_files(repo_path, commit_hash):
    cmd = ["git", "show", "--name-only", "--pretty=format:", commit_hash]
    result = subprocess.run(cmd, cwd=repo_path, capture_output=True, text=True, check=True)
    files = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    return files

def build_dependency_graph(repo_path, commits):
    graph = []
    for commit in commits:
        files = get_commit_files(repo_path, commit)
        graph.append((commit, files))
    return graph

def generate_mermaid(graph):
    mermaid = ["graph TD"]
    for commit, files in graph:
        node_id = commit[:7]
        for file in files:
            mermaid.append(f"    {node_id}([Commit {node_id}]):::commit --> |Files| {file}")
    return "\n".join(mermaid)

def save_mermaid_to_file(mermaid):
    with open("test.mmd", 'w') as tmp_file:
        tmp_file.write(mermaid)
        return tmp_file.name

def generate_graph_image(graphviz_path, mermaid_file, output_path):
    cmd = [graphviz_path, "-o", output_path, "-i", mermaid_file]
    subprocess.run(cmd, check=True)

def main():
    args = parse_arguments()

    if not os.path.exists(args.repo_path):
        raise FileNotFoundError(f"Repository path not found: {args.repo_path}")
    if not os.path.exists(args.graphviz_path):
        raise FileNotFoundError(f"Graph visualization program not found: {args.graphviz_path}")

    commits = get_git_commits(args.repo_path, args.since_date)
    graph = build_dependency_graph(args.repo_path, commits)

    mermaid = generate_mermaid(graph)
    mermaid_file = save_mermaid_to_file(mermaid)

    generate_graph_image(args.graphviz_path, mermaid_file, args.output_path)

    print(f"Dependency graph successfully generated and saved to {args.output_path}")

if __name__ == "__main__":
    main()