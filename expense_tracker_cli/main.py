from expense import Expense
import argparse
import logging
import sys

logging.basicConfig(level=logging.INFO,format="%(levelname)s %(asctime)s %(message)s")
logger = logging.getLogger(__name__)


parser = argparse.ArgumentParser()
parser.add_argument("command",help="specify add,update,list,delete command",type=str)
parser.add_argument("--description",help="add description of each expense",type=str)
parser.add_argument("--amount",help="add amount to each amount",type=float)
parser.add_argument("--id",help="fetch each expense by unique id",type=int)
parser.add_argument("--summary",help="summarize all expenses")
parser.add_argument("--month",help="specify the month to summarize",type=int)

def options(args,expense):
    if args.description and args.amount:
        expense.description = args.description
        expense.amount = args.amount
        logger.info(f"Description: {expense.description} & Amount: {expense.amount}")
    
    elif args.description and not args.amount:
        expense.description = args.description
        logger.info(f"Description: {expense.description} only")
    
    elif args.amount and not args.description:
        expense.amount = args.amount
        logger.info(f"Amount: {expense.amount}")

args = parser.parse_args()

expense = Expense()

if args.command == "list":
    logger.info("list expense")
    expense.get_all()

elif args.command == "add":
    logger.info("add expense")
    options(args,expense)
    expense.create()

elif args.command == "update":
    logger.info("updatin expense")
    options(args,expense)
    if args.id:
        expense.update(
            args.id,
            expense.description,
            expense.amount
        )

elif args.command == "delete":
    logger.info("deletin expense")
    if args.id:
        expense.delete(args.id)

elif args.command == "summary":
    logger.info("summarize expense")
    if args.month:
        expense.summary(filter=args.month)
    else:
        expense.summary()

else:
    logging.error("invalid command: Use py main.py -h")