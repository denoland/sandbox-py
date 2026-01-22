import io
import pytest


@pytest.mark.asyncio(loop_scope="session")
async def test_fs_file_write_read_async(async_shared_sandbox):
    sb = async_shared_sandbox
    path = "test_fsfile_async.txt"

    # Create a file and write to it
    await sb.fs.write_text_file(path, "")
    async with await sb.fs.open(path, read=True, write=True) as f:
        bytes_written = await f.write(b"hello world")
        assert bytes_written == 11

        # Seek to beginning and read
        await f.seek(0, io.SEEK_SET)
        content = await f.read(11)
        assert content == b"hello world"


def test_fs_file_write_read_sync(shared_sandbox):
    sb = shared_sandbox
    path = "test_fsfile_sync.txt"

    # Create a file and write to it
    sb.fs.write_text_file(path, "")
    with sb.fs.open(path, read=True, write=True) as f:
        bytes_written = f.write(b"hello world")
        assert bytes_written == 11

        # Seek to beginning and read
        f.seek(0, io.SEEK_SET)
        content = f.read(11)
        assert content == b"hello world"


@pytest.mark.asyncio(loop_scope="session")
async def test_fs_file_seek_async(async_shared_sandbox):
    sb = async_shared_sandbox
    path = "test_seek_async.txt"

    await sb.fs.write_text_file(path, "0123456789")
    async with await sb.fs.open(path, read=True) as f:
        # Seek from start
        pos = await f.seek(5, io.SEEK_SET)
        assert pos == 5
        content = await f.read(5)
        assert content == b"56789"

        # Seek from current position
        await f.seek(0, io.SEEK_SET)
        await f.seek(3, io.SEEK_CUR)
        content = await f.read(3)
        assert content == b"345"


def test_fs_file_seek_sync(shared_sandbox):
    sb = shared_sandbox
    path = "test_seek_sync.txt"

    sb.fs.write_text_file(path, "0123456789")
    with sb.fs.open(path, read=True) as f:
        # Seek from start
        pos = f.seek(5, io.SEEK_SET)
        assert pos == 5
        content = f.read(5)
        assert content == b"56789"

        # Seek from current position
        f.seek(0, io.SEEK_SET)
        f.seek(3, io.SEEK_CUR)
        content = f.read(3)
        assert content == b"345"


@pytest.mark.asyncio(loop_scope="session")
async def test_fs_file_truncate_async(async_shared_sandbox):
    sb = async_shared_sandbox
    path = "test_truncate_async.txt"

    await sb.fs.write_text_file(path, "hello world")
    async with await sb.fs.open(path, read=True, write=True) as f:
        # Truncate to 0 (clear the file)
        await f.truncate(0)

    content = await sb.fs.read_text_file(path)
    assert content == ""


def test_fs_file_truncate_sync(shared_sandbox):
    sb = shared_sandbox
    path = "test_truncate_sync.txt"

    sb.fs.write_text_file(path, "hello world")
    with sb.fs.open(path, read=True, write=True) as f:
        # Truncate to 0 (clear the file)
        f.truncate(0)

    content = sb.fs.read_text_file(path)
    assert content == ""


@pytest.mark.asyncio(loop_scope="session")
async def test_fs_file_stat_async(async_shared_sandbox):
    sb = async_shared_sandbox
    path = "test_stat_async.txt"

    await sb.fs.write_text_file(path, "hello")
    async with await sb.fs.open(path, read=True) as f:
        stat = await f.stat()
        assert stat["is_file"] is True
        assert stat["size"] == 5


def test_fs_file_stat_sync(shared_sandbox):
    sb = shared_sandbox
    path = "test_stat_sync.txt"

    sb.fs.write_text_file(path, "hello")
    with sb.fs.open(path, read=True) as f:
        stat = f.stat()
        assert stat["is_file"] is True
        assert stat["size"] == 5


@pytest.mark.asyncio(loop_scope="session")
async def test_fs_file_sync_data_async(async_shared_sandbox):
    sb = async_shared_sandbox
    path = "test_syncdata_async.txt"

    await sb.fs.write_text_file(path, "")
    async with await sb.fs.open(path, write=True) as f:
        await f.write(b"test data")
        await f.sync_data()  # Should not raise


def test_fs_file_sync_data_sync(shared_sandbox):
    sb = shared_sandbox
    path = "test_syncdata_sync.txt"

    sb.fs.write_text_file(path, "")
    with sb.fs.open(path, write=True) as f:
        f.write(b"test data")
        f.sync_data()  # Should not raise


@pytest.mark.asyncio(loop_scope="session")
async def test_fs_file_lock_unlock_async(async_shared_sandbox):
    sb = async_shared_sandbox
    path = "test_lock_async.txt"

    await sb.fs.write_text_file(path, "content")
    async with await sb.fs.open(path, read=True, write=True) as f:
        await f.lock(True)  # Exclusive lock
        await f.unlock()


def test_fs_file_lock_unlock_sync(shared_sandbox):
    sb = shared_sandbox
    path = "test_lock_sync.txt"

    sb.fs.write_text_file(path, "content")
    with sb.fs.open(path, read=True, write=True) as f:
        f.lock(True)  # Exclusive lock
        f.unlock()
