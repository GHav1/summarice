import sys
from book_library import add_book

if __name__ == "__main__":
    book_name = sys.argv[1]
    author_name = sys.argv[2]
    content = sys.argv[3]
    result = add_book(book_name, author_name, content)
    print(result)
