import hashlib
from nexus import Agent, Bureau, Context, Model
from nexus.crypto import Identity


class Message(Model):
    message: str
    digest: bytes
    signature: str


def encode(message: str) -> bytes:
    hasher = hashlib.sha256()
    hasher.update(message.encode())
    return hasher.digest()


alice = Agent(name="alice", seed="alice recovery password")
bob = Agent(name="bob", seed="bob recovery password")

assert (
    alice.address == "agent1qg985el6kquqw3zdnq7tvpsz2n0srxa8e8eyp0nwpagp6yyg2ayus294dux"
)
assert (
    bob.address == "agent1qgqdlpds2w7rs032jgylcka8m5d663nvt6p5dmmffpmanljldchssyjhn9r"
)


@alice.on_interval(period=3.0)
async def send_message(ctx: Context):
    msg = "hello there bob"
    digest = encode(msg)
    await ctx.send(
        bob.address,
        Message(message=msg, digest=digest, signature=alice.sign_digest(digest)),
    )


@alice.on_message(model=Message)
async def alice_rx_message(ctx: Context, sender: str, msg: Message):
    assert Identity.verify_digest(
        sender, msg.digest, msg.signature
    ), "couldn't verify bob's message"

    print("Bob's message verified!")
    print(f"[{ctx.name:5}] From: {sender} {msg.message}")


@bob.on_message(model=Message)
async def bob_rx_message(ctx: Context, sender: str, msg: Message):
    assert Identity.verify_digest(
        sender, msg.digest, msg.signature
    ), "couldn't verify alice's message"
    print("Alice's message verified!")

    print(f"[{ctx.name:5}] From: {sender} {msg.message}")

    msg = "hello there alice"
    digest = encode(msg)

    # send the response
    await ctx.send(
        alice.address,
        Message(message=msg, digest=digest, signature=bob.sign_digest(digest)),
    )


# since we have multiple agents in this example we add them to a bureau
# (just an "office" for agents)
bureau = Bureau()
bureau.add(alice)
bureau.add(bob)

if __name__ == "__main__":
    bureau.run()