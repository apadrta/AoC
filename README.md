# Advent of code

* URL: [https://adventofcode.com/](https://adventofcode.com/)
* Time: each year 1.-25. December
* Solutions
	* [2019](advent_of_code_2019/)
	* [2020](advent_of_code_2020/)
	* [2021](advent_of_code_2021/)
	* [2022](advent_of_code_2022/)
* File naming conventions 
	* `input_check.txt` - example data for testing
	* `input.txt` - real data
	* `*.py` - solution scripts
	* `task.txt` - task description 


## Dicta Adventus Codicis

* prozkoumejte si vždy vstupní data, ať máte představu v jakých řádech se budete pohybovat (počty, rozsahy) a podle toho zvolte upočitatelné řešení
* neprogramujte nehospodárně jako microsoft nebo typičtí javisti a vyhněte se co nejvíc všem náročným operacím (sekvenční prohledávání dlouhého pole apod.)
* vhodně zvolte reprezentaci vstupních dat v paměti
* nepřesouvejte data tam a zpět, místo toho pro strukturu použijte spojový seznam nebo ukazatele (indexy)
* nahraďte rekurzivní funkce cykly (jakoukoli rekurzi lze nahradit cyklem)
* nahraďte cykly násobením, když to lze
  * příklad: x = 100 * N místo for i in range(0, N): x += 1
  * dá se použít v mnoha případech / variantách
* používejte break a continue k ukončení „neperspektivních“ částí
* zkuste využít již vypočítaná data (ukládejte výsledky opakujících se částí získaných náročným výpočtem)
* zkuste se zaměřit pouze na data nezbytná pro řešení

