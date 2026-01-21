import io
import pytest


@pytest.mark.asyncio(loop_scope="session")
async def test_write_file_bytes_async(async_shared_sandbox):
    """Test write_file with bytes (existing behavior)."""
    sb = async_shared_sandbox

    await sb.fs.write_file("test_bytes.txt", b"hello world")
    content = await sb.fs.read_file("test_bytes.txt")
    assert content == b"hello world"


def test_write_file_bytes_sync(shared_sandbox):
    """Test write_file with bytes (existing behavior)."""
    sb = shared_sandbox

    sb.fs.write_file("test_bytes_sync.txt", b"hello world")
    content = sb.fs.read_file("test_bytes_sync.txt")
    assert content == b"hello world"


@pytest.mark.asyncio(loop_scope="session")
async def test_write_file_generator_async(async_shared_sandbox):
    """Test write_file with a sync generator."""
    sb = async_shared_sandbox

    def chunks():
        yield b"hello "
        yield b"world"

    await sb.fs.write_file("test_generator.txt", chunks())
    content = await sb.fs.read_file("test_generator.txt")
    assert content == b"hello world"


def test_write_file_generator_sync(shared_sandbox):
    """Test write_file with a sync generator."""
    sb = shared_sandbox

    def chunks():
        yield b"hello "
        yield b"world"

    sb.fs.write_file("test_generator_sync.txt", chunks())
    content = sb.fs.read_file("test_generator_sync.txt")
    assert content == b"hello world"


@pytest.mark.asyncio(loop_scope="session")
async def test_write_file_async_generator(async_shared_sandbox):
    """Test write_file with an async generator."""
    sb = async_shared_sandbox

    async def async_chunks():
        yield b"async "
        yield b"hello "
        yield b"world"

    await sb.fs.write_file("test_async_generator.txt", async_chunks())
    content = await sb.fs.read_file("test_async_generator.txt")
    assert content == b"async hello world"


@pytest.mark.asyncio(loop_scope="session")
async def test_write_file_file_object_async(async_shared_sandbox):
    """Test write_file with a file-like object."""
    sb = async_shared_sandbox

    file_obj = io.BytesIO(b"file object content")
    await sb.fs.write_file("test_file_obj.txt", file_obj)
    content = await sb.fs.read_file("test_file_obj.txt")
    assert content == b"file object content"


def test_write_file_file_object_sync(shared_sandbox):
    """Test write_file with a file-like object."""
    sb = shared_sandbox

    file_obj = io.BytesIO(b"file object content sync")
    sb.fs.write_file("test_file_obj_sync.txt", file_obj)
    content = sb.fs.read_file("test_file_obj_sync.txt")
    assert content == b"file object content sync"


@pytest.mark.asyncio(loop_scope="session")
async def test_write_file_list_async(async_shared_sandbox):
    """Test write_file with a list of bytes."""
    sb = async_shared_sandbox

    chunks = [b"part1 ", b"part2 ", b"part3"]
    await sb.fs.write_file("test_list.txt", iter(chunks))
    content = await sb.fs.read_file("test_list.txt")
    assert content == b"part1 part2 part3"


def test_write_file_list_sync(shared_sandbox):
    """Test write_file with a list of bytes."""
    sb = shared_sandbox

    chunks = [b"part1 ", b"part2 ", b"part3"]
    sb.fs.write_file("test_list_sync.txt", iter(chunks))
    content = sb.fs.read_file("test_list_sync.txt")
    assert content == b"part1 part2 part3"


@pytest.mark.asyncio(loop_scope="session")
async def test_write_file_empty_stream_async(async_shared_sandbox):
    """Test write_file with an empty stream."""
    sb = async_shared_sandbox

    def empty_chunks():
        return
        yield  # Make it a generator

    await sb.fs.write_file("test_empty.txt", empty_chunks())
    content = await sb.fs.read_file("test_empty.txt")
    assert content == b""


def test_write_file_empty_stream_sync(shared_sandbox):
    """Test write_file with an empty stream."""
    sb = shared_sandbox

    def empty_chunks():
        return
        yield  # Make it a generator

    sb.fs.write_file("test_empty_sync.txt", empty_chunks())
    content = sb.fs.read_file("test_empty_sync.txt")
    assert content == b""


@pytest.mark.asyncio(loop_scope="session")
async def test_write_file_large_stream_async(async_shared_sandbox):
    """Test write_file with a stream larger than chunk size."""
    sb = async_shared_sandbox

    # Create a generator that yields 100KB total (larger than 64KB default chunk)
    def large_chunks():
        for i in range(10):
            yield b"x" * 10240  # 10KB per chunk

    await sb.fs.write_file("test_large.txt", large_chunks())
    content = await sb.fs.read_file("test_large.txt")
    assert len(content) == 102400
    assert content == b"x" * 102400


def test_write_file_large_stream_sync(shared_sandbox):
    """Test write_file with a stream larger than chunk size."""
    sb = shared_sandbox

    # Create a generator that yields 100KB total (larger than 64KB default chunk)
    def large_chunks():
        for _ in range(10):
            yield b"x" * 10240  # 10KB per chunk

    sb.fs.write_file("test_large_sync.txt", large_chunks())
    content = sb.fs.read_file("test_large_sync.txt")
    assert len(content) == 102400
    assert content == b"x" * 102400
