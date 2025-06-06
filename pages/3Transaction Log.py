from core.db import check_authentication, render_sidebar, render_transaction_logs

def main():
    check_authentication()
    render_sidebar()
    render_transaction_logs()

if __name__ == "__main__":
    main()