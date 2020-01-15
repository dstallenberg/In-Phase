# -*- coding: utf-8 -*-
"""
Created on Wo Jan 15 12:00:00 2020

@author: Dimitri
"""
from concurrent.futures import as_completed, ProcessPoolExecutor


def async_calls(function, arguments):
    workers = 20
    result_vector = []
    #print(arguments)
    with ProcessPoolExecutor(max_workers=workers) as executor:
        futures = []

        for i in range(len(arguments)):
            futures.append(executor.submit(function, *arguments[i]))

        for future in futures:
            result_vector.append(future.result())
        # Wait for the results of all threads
        # for future in as_completed(futures):
        #     result_vector.append(future.result())

    print('All jobs done')
    return result_vector
