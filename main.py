from typing import List, Dict, Any
from dataclasses import dataclass
import uuid


# Define commands
@dataclass
class Command:
    pass


@dataclass
class CreateAccountCommand(Command):
    account_id: str


@dataclass
class DepositMoneyCommand(Command):
    account_id: str
    amount: float


@dataclass
class WithdrawMoneyCommand(Command):
    account_id: str
    amount: float


# Define queries
@dataclass
class Query:
    pass


@dataclass
class GetAccountBalanceQuery(Query):
    account_id: str


# Define command handlers
class CommandHandler:
    def handle(self, command: Command):
        pass


class CreateAccountCommandHandler(CommandHandler):
    def handle(self, command: CreateAccountCommand):
        # Simulate creating an account in a database
        return {"account_id": command.account_id, "balance": 0.0}


class DepositMoneyCommandHandler(CommandHandler):
    def handle(self, command: DepositMoneyCommand):
        # Simulate updating the account balance in a database
        return {"account_id": command.account_id, "balance": command.amount}


class WithdrawMoneyCommandHandler(CommandHandler):
    def handle(self, command: WithdrawMoneyCommand):
        # Simulate updating the account balance in a database
        return {"account_id": command.account_id, "balance": -command.amount}


# Define query handlers
class QueryHandler:
    def handle(self, query: Query):
        pass


class GetAccountBalanceQueryHandler(QueryHandler):
    def handle(self, query: GetAccountBalanceQuery):
        # Simulate querying the account balance from a database
        return {"account_id": query.account_id, "balance": 100.0}


# Define a simple CQRS bus
class CQRSBus:
    def __init__(self):
        self.command_handlers: Dict[str, CommandHandler] = {}
        self.query_handlers: Dict[str, QueryHandler] = {}

    def register_command_handler(self, command_cls: type, handler: CommandHandler):
        self.command_handlers[command_cls.__name__] = handler

    def register_query_handler(self, query_cls: type, handler: QueryHandler):
        self.query_handlers[query_cls.__name__] = handler

    def execute_command(self, command: Command) -> Any:
        handler = self.command_handlers.get(command.__class__.__name__)
        if handler:
            return handler.handle(command)
        else:
            raise ValueError(f"No handler registered for command: {command.__class__.__name__}")

    def execute_query(self, query: Query) -> Any:
        handler = self.query_handlers.get(query.__class__.__name__)
        if handler:
            return handler.handle(query)
        else:
            raise ValueError(f"No handler registered for query: {query.__class__.__name__}")


# Example usage
if __name__ == "__main__":
    cqrs_bus = CQRSBus()
    cqrs_bus.register_command_handler(CreateAccountCommand, CreateAccountCommandHandler())
    cqrs_bus.register_command_handler(DepositMoneyCommand, DepositMoneyCommandHandler())
    cqrs_bus.register_command_handler(WithdrawMoneyCommand, WithdrawMoneyCommandHandler())
    cqrs_bus.register_query_handler(GetAccountBalanceQuery, GetAccountBalanceQueryHandler())

    # Create an account
    account_id = str(uuid.uuid4())
    create_account_command = CreateAccountCommand(account_id)
    result = cqrs_bus.execute_command(create_account_command)
    print(f"Created account with ID: {result['account_id']}")

    # Deposit money
    deposit_command = DepositMoneyCommand(account_id, 50.0)
    result = cqrs_bus.execute_command(deposit_command)
    print(f"Deposited $50.0 into account {result['account_id']}")

    # Withdraw money
    withdraw_command = WithdrawMoneyCommand(account_id, 30.0)
    result = cqrs_bus.execute_command(withdraw_command)
    print(f"Withdrew $30.0 from account {result['account_id']}")

    # Query account balance
    query = GetAccountBalanceQuery(account_id)
    result = cqrs_bus.execute_query(query)
    print(f"Account {result['account_id']} balance: ${result['balance']}")
