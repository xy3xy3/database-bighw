from jinja2 import Environment, FileSystemLoader, select_autoescape
from fastapi.templating import Jinja2Templates


class Templates(Jinja2Templates):
    def __init__(self, directory: str) -> None:
        super().__init__(directory)

        # 配置 Jinja2 环境
        env = Environment(
            loader=FileSystemLoader(directory),
            autoescape=select_autoescape(['html', 'xml'])
        )
        env.block_start_string = '<%'
        env.block_end_string = '%>'
        env.variable_start_string = '<<'
        env.variable_end_string = '>>'

        self.env = env
