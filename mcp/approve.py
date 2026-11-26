"""Human-only terminal approval. Never registered as a model tool."""
import sys
import approvals


def main():
    if len(sys.argv) != 2 or not sys.stdin.isatty():
        raise SystemExit("Use um terminal interativo: python mcp/approve.py PROPOSTA")
    proposal_id = sys.argv[1]
    row = approvals._store_get(proposal_id)
    if not row or row["status"] != "pending":
        raise SystemExit("Proposta ausente ou ja decidida")
    print(row["summary"])
    if input("Para autorizar esta acao real, digite o ID da proposta: ").strip() != proposal_id:
        raise SystemExit("Acao cancelada")
    print(approvals.approve_proposal(proposal_id))


if __name__ == "__main__":
    main()
