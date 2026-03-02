import asyncio

HOST = "127.0.0.1"
PORT = 65432


async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    """
    Corrotina chamada pelo Event Loop para cada nova conexão.
    """
    addr = writer.get_extra_info("peername")
    print(f"[NOVA CONEXÃO] {addr}")

    try:
        # 1) Ler dados do cliente (até 1024 bytes)
        data = await reader.read(1024)
        msg = data.decode(errors="replace").strip()

        # 2) Simular processamento pesado SEM bloquear a thread principal
        # (usa o event loop; não use time.sleep)
        await asyncio.sleep(5)

        # 3) Responder ao cliente
        response = f"OK - recebido: {msg}\n"
        writer.write(response.encode())
        await writer.drain()

    except Exception as e:
        print(f"[ERRO] {addr} -> {e}")

    finally:
        # 4) Fechar conexão
        try:
            writer.close()
            await writer.wait_closed()
        except Exception:
            pass

        print(f"[DESCONECTADO] {addr}")


async def main():
    # Criar servidor assíncrono
    server = await asyncio.start_server(handle_client, HOST, PORT)

    addrs = ", ".join(str(sock.getsockname()) for sock in server.sockets or [])
    print(f"[ASSÍNCRONO] Servidor rodando em {addrs} — Event Loop ativo.")

    # Manter rodando indefinidamente
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())