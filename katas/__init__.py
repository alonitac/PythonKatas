katas = {
    "intro": {  # take the bus to the general store
        "steps": 20,
        "icon_class": "fas fa-bus-alt",
        "katas": [
            ('hello_world.py', 'function structure'),
            ('hello_world2.py', 'str type, concat'),
            ('numbers_division.py', 'int, float'),
            ('personalized_hello_world.py', 'func args'),
            ('age_message_fix.py', 'dynamically typed, + operator'),
            ('get_seconds.py', 'math'),
            ('get_century.py', 'math'),
            ('bad_average.py', 'parentheses'),
            ('calculator1.py', 'built-in funcs, func call'),
            ('calculator2.py', 'convert types'),
            ('tax_calc.py', 'multiple fuc args, scope'),
            ('bad_function.py', 'troubleshoot'),
        ]
    },
    "controlflow": {  # bicycle to Lamothe's Garage
        "steps": 40,
        "icon_class": "fas fa-bicycle",
        "katas": [
            ('fill_a_cab.py', 'simple if'),
            ('time_convertor.py', 'elif and ==='),
            ('is_even.py', 'bool'),
            ('can_drive.py', 'and'),
            ('can_drive2.py', 'or operators'),
            ('assess_temperature.py', 'if else elif'),
            ('my_abs.py', 'abs'),
            ('shopping_list.py', 'list'),
            ('last_one.py', 'list index'),
            ('sandwich_ingredients.py', 'slice'),
            ('every_second_word.py', 'slice with jumps'),
            ('recent_messages.py', 'slice to ends'),
            ('get_username.py', 'slice of string'),
            ('shopping_list2.py', 'list append'),
            ('log_message.py', 'print vs return'),
            ('', 'default args'),
            ('mailing_list.py', 'concat and split'),
            ('grader.py', 'multiple returns'),
            ('find_student.py', 'in operator'),
            ('is_word_absent.py', 'not in'),
            ('is_valid_password', 'len built-in'),
            ('is_earlier.py', 'compare lists'),
            ('num_of_digits.py', 'int to str conversion'),
            ('is_palindrome.py', 'reverse string'),
            ('has_pattern.py', 'slice in if'),
            ('is_subscriber_matching.py', 'case-insensitive str'),
            ('get_first_n_words.py', 'split, join'),
            ('clean_text.py', 'replace'),
            ('get_user_info.py', 'tuple, return multiple values'),
            ('fraction_of_float.py', 'type conversion'),
            ('start_end.py', 'slice, str, user input'),
            ('verbing.py', 'str endswith'),
        ]
    },
    "loops": {  # truck to the beginning of the hiking
        "steps": 40,
        "icon_class": "fas fa-truck-pickup",
        "katas": [
            ('print_list_elements.py', 'for loop'),
            ('total_expense.py', 'for with aggregator variable'),
            ('min_max.py', 'max, min implementation with for loops'),
            ('mailing_list2.py', 'override element in a list'),
            ('is_prime.py', 'built in: range'),
            ('list_diff.py', 'for loop with range() index'),
            ('under_18.py', 'counter outside loop'),
            ('even_sublist.py', 'for loop'),
            ('word_count.py', 'word count'),
            ('sum_even_numbers.py', 'fix error (range(lst) instead range(len(lst)))'),
            ('app_health.py', 'global variable'),
            ('max_difference.py', 'for in for'),
            ('name_pair.py', 'all pairs in a list (for in for)'),
            ('validate_age.py', 'user input validation, isinstance()'),
            ('is_unique_str.py', 'set: is unique str'),
            ('reformat_phone.py', 'reformat phone number: isdigit()'),
            ('swap_in_list.py', 'swap'),
            ('partial_list.py', 'partial list'),
            ('lottery_guess.py', 'import random'),
            ('summarize_scores.py', 'function declaration'),
            ('all_positive.py', 'all() built in'),
            ('long_str.py', 'any() built in'),
        ]
    },
    "datastructures": {  # hike to the beach
        "steps": 50,
        "icon_class": "far fa-hiking",
        "katas": [
            ('currency_convert.py', 'dict intro: convert currency'),
            ('get_department.py', 'get value by key'),
            ('course_enrollment.py', 'working with two dicts'),
            ('contacts.py', 'keys assign, dict mutability'),
            ('phone_lookup.py', 'dict: in operator, get()'),
            ('fix_movie_review.py', 'check if key is in dict (fix common error)'),
            ('overweight.py', 'dict.items()'),
            ('find_item_price.py', 'nested dict'),
            ('check_identity.py', 'the `is` operator'),
            ('book_your_seat.py', 'is None'),
            ('boarding_pass_code.py', 'f string'),
            ('process_payment.py', 'type() or isinstance(): multiple input type for an argument'),
            ('lets_vote.py', 'increase counter in dict (add if not exist)'),
            ('in_the_club.py', 'check if key exist in dict'),
            ('top_student.py', 'lambda introduced'),
            ('mind_the_gap.py', 'str.count() manually'),
            ('is_sublist.py', 'sublist check'),
            ('runner_position.py', 'list.index() manually'),
            ('folder_count.py', 'path manipulation'),
            ('secret_club.py', 'zip() - dict from two lists'),
            ('dicts_in_order.py', 'list of tuples from dict'),
            ('they_legit.py', 'list of dict, lambda functions'),
            ('count_even_numbers.py', 'return terminates the function (bug)'),
            ('do_twice.py', 'pointer to function'),
            ('list_rotation.py', 'list rotation'),
            ('time_me.py', 'import time'),
            ('monotonic_array.py', ''),
            ('prime_num.py', ''),
            ('seven_boom.py', ''),
            ('strong_pass.py', 're'),
            ('merge_sorted_lists.py', 'sort and sorted'),
            ('best_student.py', ''),
            ('pair_match.py', ''),
            ('merge_dict.py', 'merge dicts'),
        ]
    },
    "io_errorhandling": {  # io and error handling
        "steps": 20,
        "icon_class": "fas fa-helicopter",
        "katas": [
            ('tmp.py', ''),
        ]
    },
    "classes": {  # io and error handling
        "steps": 20,
        "icon_class": "fa-person-swimming",
        "katas": [
            ('tmp.py', ''),
        ]
    }
}

### to combine within regular katas

    # os module
    # files Path
    # graceful termintion
    # regex (with a link to learn regex)
    # dates and time
    # logigng

###

    # flask
    # modules and packages
    # cli
    # requests
    # working with api
    # algorithmic questions

"""
    ('', 'toward binary search'),
    ('', 'add if not exists (list and dict) (set)'),
fix_me.py
knapsack.py
tasks_scheduling.py
pascal_triangle.py
youtube.py
bash.py
count_vowels.py
to_lower_case.py
complete_me.py
sum_of_elements.py
words_concat.py

summer.py

files_backup.py
most_frequent_name.py
replace_in_file.py
github_status.py
reviewed_pull_requests.py
file_exceptions.py
binary_to_dec.py
is_valid_email.py
car.py
dog.py
cache_list.py
simple_queue.py
util_package.py
custom_import.py
import_warning.py
start_end_v2.py
sum_of_digits.py
reverse_words_concat.py
matrix_avg.py
do_n_times.py
ceaser_cipher.py
is_unique_str.py
merge_dict_v2.py
name_histogram.py
scrooge_customers.py
sjf.py
nginx_log_parser.py
json_configs_merge.py
requests_retry.py
requests_timeout.py
tree.py
sorted_dict.py
custom_exception.py
messy_module.py
list_flatten.py
longest_common_prefix.py
rotate_matrix.py
longest_common_substring.py
valid_parentheses.py
valid_git_tree.py
ansible_dynamic_inv.py
queue_with_failover.py
unittesting.py
singleton.py
"""
