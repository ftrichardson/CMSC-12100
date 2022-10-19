class Library:

    def __init__(self, island, name, reference, book, microform):
        '''
        Constructor for the Library class
        '''
        self.name = name
        self.island = island
        self.reference = reference
        self.book = book
        self.microform = microform
    
    def total_circulation(self):
        '''
        Computes the total number of items in circulation at the library
        '''
        return self.reference + self.book + self.microform
    
    def has_microform_catalogue(self):
        '''
        Determines if library has any microform catalogues
        '''
        return self.microform > 0

### FUNCTIONS ###

def branch_with_biggest_circulation(libraries):
    '''
    Find the library with the largest total number of
    items in circulation

    Input:
        libraries: (list of Library) libraries

    Returns: name of library (string)
    '''
    largest_circulation = float('-inf')
    library_with_largest_circulation = None

    for library in libraries:
        if library.total_circulation() > largest_circulation:
            largest_circulation = library.total_circulation()
            library_with_largest_circulation = library
    
    return library_with_largest_circulation.name

def percentage_with_microform(libraries):
    '''
    Find the percentage of libraries that have 
    microform catalogues

    Input:
        libraries: (list of Library) libraries

    Returns: percentage (float)
    '''
    libraries_with_microform = 0

    for library in libraries:
        if library.has_microform_catalogue():
            libraries_with_microform += 1
    
    return (libraries_with_microform / len(libraries)) * 100