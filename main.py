from SRS import SRS

def main():
    test_srs_path = "test.srs"
    test_srs = SRS()
    test_srs.load_terms_from_file(test_srs_path)
    
    test_srs.print_terms()


main()