#import readnovelfull
from Sources.pichau import pichau

# define available sources, must have a class created in folder
available_souces = {
    'Pichau': pichau
}

def search_product(search_query: str):
    results = []
    
    for source in available_souces:
        print(f"Checking website '{source}'...")
        # create an instance of the class
        source_instance = available_souces[source]()

        # call the search_product method on the instance
        results += source_instance.search_product(search_query)

        return results
    #end for
    return None
#end def
    
