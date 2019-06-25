from os.path import join
from bountydns.core.utils import db_dir, load_env
from bountydns.db.session import session, db_register
from bountydns.db.utils import make_db_url
from bountydns.db.migrate.downgrade import downgrade
from bountydns.cli.base import BaseCommand


class AlembicDowngrade(BaseCommand):
    name = "alembic-downgrade"
    aliases = ["al-downgrade"]
    description = "run alembic downgrade"
    migration_dir = join(db_dir("alembic"), "api")

    @classmethod
    def parser(cls, parser):
        return parser

    async def run(self):
        env = self.option("env")
        self.load_env(f"api.{env}")
        db_register(make_db_url())
        downgrade(self.migration_dir)