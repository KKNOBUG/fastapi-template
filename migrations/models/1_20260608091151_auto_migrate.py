from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `krun_user` ADD `token_version` INT NOT NULL  COMMENT 'Token版本号，用于吊销用户所有Token' DEFAULT 0;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `krun_user` DROP COLUMN `token_version`;"""
