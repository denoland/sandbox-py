import io
import os
import tempfile
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


# stdin streaming tests for spawn


@pytest.mark.asyncio(loop_scope="session")
async def test_spawn_stdin_stream_async(async_shared_sandbox):
    """Test spawn with stdin stream (async)."""
    sb = async_shared_sandbox

    def stdin_chunks():
        yield b"hello from stdin"

    p = await sb.spawn(
        "cat",
        stdout="piped",
        stderr="piped",
        stdin_data=stdin_chunks(),
    )

    status = await p.wait()
    assert status["code"] == 0

    stdout = await p.stdout.read(-1)
    assert stdout == b"hello from stdin"


def test_spawn_stdin_stream_sync(shared_sandbox):
    """Test spawn with stdin stream (sync)."""
    sb = shared_sandbox

    def stdin_chunks():
        yield b"hello from stdin sync"

    p = sb.spawn(
        "cat",
        stdout="piped",
        stderr="piped",
        stdin_data=stdin_chunks(),
    )

    status = p.wait()
    assert status["code"] == 0

    stdout = p.stdout.read(-1)
    assert stdout == b"hello from stdin sync"


@pytest.mark.asyncio(loop_scope="session")
async def test_spawn_stdin_file_object_async(async_shared_sandbox):
    """Test spawn with stdin as file-like object (async)."""
    sb = async_shared_sandbox

    file_obj = io.BytesIO(b"stdin from file object")

    p = await sb.spawn(
        "cat",
        stdout="piped",
        stderr="piped",
        stdin_data=file_obj,
    )

    status = await p.wait()
    assert status["code"] == 0

    stdout = await p.stdout.read(-1)
    assert stdout == b"stdin from file object"


def test_spawn_stdin_file_object_sync(shared_sandbox):
    """Test spawn with stdin as file-like object (sync)."""
    sb = shared_sandbox

    file_obj = io.BytesIO(b"stdin from file object sync")

    p = sb.spawn(
        "cat",
        stdout="piped",
        stderr="piped",
        stdin_data=file_obj,
    )

    status = p.wait()
    assert status["code"] == 0

    stdout = p.stdout.read(-1)
    assert stdout == b"stdin from file object sync"


# stdin streaming tests for deno.run


@pytest.mark.asyncio(loop_scope="session")
async def test_deno_run_stdin_stream_async(async_shared_sandbox):
    """Test deno.run with stdin stream (async)."""
    sb = async_shared_sandbox

    def stdin_chunks():
        yield b"deno stdin test"

    p = await sb.deno.run(
        code="""
const buf = new Uint8Array(1024);
const n = await Deno.stdin.read(buf);
if (n) {
    await Deno.stdout.write(buf.subarray(0, n));
}
""",
        stdout="piped",
        stderr="piped",
        stdin_data=stdin_chunks(),
    )

    status = await p.wait()
    assert status["code"] == 0

    stdout = await p.stdout.read(-1)
    assert stdout == b"deno stdin test"


def test_deno_run_stdin_stream_sync(shared_sandbox):
    """Test deno.run with stdin stream (sync)."""
    sb = shared_sandbox

    def stdin_chunks():
        yield b"deno stdin test sync"

    p = sb.deno.run(
        code="""
const buf = new Uint8Array(1024);
const n = await Deno.stdin.read(buf);
if (n) {
    await Deno.stdout.write(buf.subarray(0, n));
}
""",
        stdout="piped",
        stderr="piped",
        stdin_data=stdin_chunks(),
    )

    status = p.wait()
    assert status["code"] == 0

    stdout = p.stdout.read(-1)
    assert stdout == b"deno stdin test sync"


# upload tests


@pytest.mark.asyncio(loop_scope="session")
async def test_upload_file_async(async_shared_sandbox):
    """Test uploading a single file (async)."""
    sb = async_shared_sandbox

    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(b"uploaded file content")
        local_path = f.name

    try:
        await sb.fs.upload(local_path, "/tmp/uploaded_file.txt")
        content = await sb.fs.read_file("/tmp/uploaded_file.txt")
        assert content == b"uploaded file content"
    finally:
        os.unlink(local_path)


def test_upload_file_sync(shared_sandbox):
    """Test uploading a single file (sync)."""
    sb = shared_sandbox

    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(b"uploaded file content sync")
        local_path = f.name

    try:
        sb.fs.upload(local_path, "/tmp/uploaded_file_sync.txt")
        content = sb.fs.read_file("/tmp/uploaded_file_sync.txt")
        assert content == b"uploaded file content sync"
    finally:
        os.unlink(local_path)


@pytest.mark.asyncio(loop_scope="session")
async def test_upload_directory_async(async_shared_sandbox):
    """Test uploading a directory with files (async)."""
    sb = async_shared_sandbox

    with tempfile.TemporaryDirectory() as tmpdir:
        # Create some files in the directory
        with open(os.path.join(tmpdir, "file1.txt"), "wb") as f:
            f.write(b"file1 content")
        with open(os.path.join(tmpdir, "file2.txt"), "wb") as f:
            f.write(b"file2 content")

        # Create a subdirectory with a file
        subdir = os.path.join(tmpdir, "subdir")
        os.makedirs(subdir)
        with open(os.path.join(subdir, "nested.txt"), "wb") as f:
            f.write(b"nested content")

        await sb.fs.upload(tmpdir, "/tmp/uploaded_dir")

        # Verify files were uploaded
        content1 = await sb.fs.read_file("/tmp/uploaded_dir/file1.txt")
        assert content1 == b"file1 content"

        content2 = await sb.fs.read_file("/tmp/uploaded_dir/file2.txt")
        assert content2 == b"file2 content"

        nested = await sb.fs.read_file("/tmp/uploaded_dir/subdir/nested.txt")
        assert nested == b"nested content"


def test_upload_directory_sync(shared_sandbox):
    """Test uploading a directory with files (sync)."""
    sb = shared_sandbox

    with tempfile.TemporaryDirectory() as tmpdir:
        # Create some files in the directory
        with open(os.path.join(tmpdir, "file1.txt"), "wb") as f:
            f.write(b"file1 content sync")
        with open(os.path.join(tmpdir, "file2.txt"), "wb") as f:
            f.write(b"file2 content sync")

        # Create a subdirectory with a file
        subdir = os.path.join(tmpdir, "subdir")
        os.makedirs(subdir)
        with open(os.path.join(subdir, "nested.txt"), "wb") as f:
            f.write(b"nested content sync")

        sb.fs.upload(tmpdir, "/tmp/uploaded_dir_sync")

        # Verify files were uploaded
        content1 = sb.fs.read_file("/tmp/uploaded_dir_sync/file1.txt")
        assert content1 == b"file1 content sync"

        content2 = sb.fs.read_file("/tmp/uploaded_dir_sync/file2.txt")
        assert content2 == b"file2 content sync"

        nested = sb.fs.read_file("/tmp/uploaded_dir_sync/subdir/nested.txt")
        assert nested == b"nested content sync"


@pytest.mark.asyncio(loop_scope="session")
async def test_upload_symlink_async(async_shared_sandbox):
    """Test uploading a symlink (async)."""
    sb = async_shared_sandbox

    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a file and a symlink to it
        target_path = os.path.join(tmpdir, "target.txt")
        with open(target_path, "wb") as f:
            f.write(b"target content")

        link_path = os.path.join(tmpdir, "link.txt")
        os.symlink("target.txt", link_path)

        await sb.fs.upload(tmpdir, "/tmp/uploaded_symlink_dir")

        # Verify the target file was uploaded
        content = await sb.fs.read_file("/tmp/uploaded_symlink_dir/target.txt")
        assert content == b"target content"

        # Verify the symlink was created (read through symlink)
        link_info = await sb.fs.lstat("/tmp/uploaded_symlink_dir/link.txt")
        assert link_info["is_symlink"] is True


def test_upload_symlink_sync(shared_sandbox):
    """Test uploading a symlink (sync)."""
    sb = shared_sandbox

    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a file and a symlink to it
        target_path = os.path.join(tmpdir, "target.txt")
        with open(target_path, "wb") as f:
            f.write(b"target content sync")

        link_path = os.path.join(tmpdir, "link.txt")
        os.symlink("target.txt", link_path)

        sb.fs.upload(tmpdir, "/tmp/uploaded_symlink_dir_sync")

        # Verify the target file was uploaded
        content = sb.fs.read_file("/tmp/uploaded_symlink_dir_sync/target.txt")
        assert content == b"target content sync"

        # Verify the symlink was created
        link_info = sb.fs.lstat("/tmp/uploaded_symlink_dir_sync/link.txt")
        assert link_info["is_symlink"] is True
