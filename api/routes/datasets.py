from fastapi import APIRouter

from data.dataset_manager import dataset_status, download_uci

router = APIRouter(prefix="/datasets", tags=["datasets"])


@router.get("/status")
def get_dataset_status() -> dict:
    return dataset_status()


@router.post("/download/uci")
def download_uci_dataset() -> dict:
    path = download_uci()
    return {"status": "ready", "path": str(path)}
