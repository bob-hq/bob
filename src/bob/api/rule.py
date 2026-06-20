from bob.core.context import Context


class Rule:
    def __init__(
        self,
        command: str,
        depfile: None | str = None,
        deps: None | str = None,
        description: None | str = None,
        restat=False,
        generator=False,
        pool: None | str = None,
    ):
        context = Context.current()

        rule_index = context.variables.get("rule_index", 1)
        context.variables["rule_index"] = rule_index + 1

        name = f"bob-{rule_index}"
        if description is not None:
            name = "".join(c for c in description.lower() if c.isalnum()) + "-" + name

        self.name = name

        assert context.writer is not None
        context.writer.rule(
            name=name,
            command=command,
            description=description,
            depfile=depfile,
            generator=generator,
            pool=pool,
            restat=restat,
            deps=deps,
        )

    def build(
        self,
        *outputs: str,
        inputs: None | list[str] = None,
        implicit: None | list[str] = None,
        order_only: None | list[str] = None,
        implicit_outputs: None | list[str] = None,
        pool: None | str = None,
        dyndep: None | str = None,
    ):
        context = Context.current()

        assert context.writer is not None
        context.writer.build(
            outputs=[str(context.builddir / output) for output in outputs],
            rule=self.name,
            inputs=inputs,
            implicit=implicit,
            order_only=order_only,
            implicit_outputs=implicit_outputs,
            pool=pool,
            dyndep=dyndep,
        )
