import os
import mimetypes
from datetime import datetime

from supabase import create_client
from config import SUPABASE_URL, SUPABASE_ANON_KEY, TABLE_LAPORAN, BUCKET_FOTO


class SupabaseService:
    def __init__(self):
        self.client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

    def insert_laporan(self, data: dict):
        return self.client.table(TABLE_LAPORAN).insert(data).execute()

    def fetch_laporan(self):
        return (
            self.client
            .table(TABLE_LAPORAN)
            .select("*")
            .order("id", desc=True)
            .execute()
        )

    def delete_laporan(self, laporan_id: int):
        return (
            self.client
            .table(TABLE_LAPORAN)
            .delete()
            .eq("id", laporan_id)
            .execute()
        )

    def update_status(self, laporan_id: int, status: str):
        return (
            self.client
            .table(TABLE_LAPORAN)
            .update({"status": status})
            .eq("id", laporan_id)
            .execute()
        )

    def upload_foto(self, file_path: str) -> str:
        filename = os.path.basename(file_path)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        storage_path = f"{stamp}_{filename}"

        mime, _ = mimetypes.guess_type(file_path)
        if not mime:
            mime = "application/octet-stream"

        with open(file_path, "rb") as f:
            file_bytes = f.read()

        bucket = self.client.storage.from_(BUCKET_FOTO)

        bucket.upload(
            path=storage_path,
            file=file_bytes,
            file_options={"content-type": mime, "upsert": "true"},
        )

        return bucket.get_public_url(storage_path)
