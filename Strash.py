
# this algorithm takes a list of strings and dynamically finds and
# assigns them keywords by content, and returns a sorted dictornary

import nltk

def strash(raw_data):
    
    raw_data = set([words.lower() for words in raw_data])# eliminate duplicates
    phrases = {}
    
    # make quick and dirty groups to start parsing
    for phrase in raw_data:
        words = nltk.word_tokenize(phrase)
        stored = False
        for word in words:
            if not stored:
                if word in phrases:
                    phrases[word].append(phrase)
                    stored = True
                else:
                    phrases[word] = [phrase]
                    stored = True

    print(phrases)
    
    shuffled = True
    while (shuffled):
        shuffled = False
        temp_phrases = dict(phrases)
        # start checking for better fits
        for key in temp_phrases:
            if(len(phrases[key]) > 1):
                for phrase in phrases[key]:
                    for word in nltk.word_tokenize(phrase):
                        alt_key_count = 0
                        for other_phrase in phrases[key]:
                            if word in other_phrase:
                                alt_key_count += 1
                        # if a phrase has a unique word in its group, check if it can crate a new group
                        if alt_key_count == 1:
                            temp_phrases = dict(phrases)
                            for other_key in temp_phrases:
                                alt_key_count = 0
                                if len(phrases[other_key]) + 1 < len(phrases[key]):
                                    for other_phrase in phrases[other_key]:
                                        if word in other_phrase:
                                            alt_key_count += 1
                                    if alt_key_count == len(phrases[other_key]):
                                        print("Merging " +  phrase + " " + str(phrases[other_key]) + " to " + word)
                                        shuffled = True
                                        if word in phrases:
                                            phrases[word].append(phrase)
                                        else:
                                            phrases[word] = [phrase]
                                        phrases[key].remove(phrase)
                                        for other_phrase in phrases[other_key]:
                                            phrases[word].append(other_phrase)
                                            phrases[other_key].remove(other_phrase)
                                            
                        # checks for sub group and strips                     
                        elif alt_key_count > 1 and alt_key_count < len(phrases[key]) and word not in phrases:
                            shuffled = True
                            print("Stripping out " + phrase + " and " + str(alt_key_count))
                            for m_phrase in phrases[key]:
                                if word in m_phrase:
                                    if word in phrases:
                                        phrases[word].append(m_phrase)
                                    else:
                                        phrases[word] = [m_phrase]
                                    phrases[key].remove(m_phrase)
            # if any groups are now empty, remove them
            if len(phrases[key]) < 1:
                phrases.pop(key)
                
        # if there have been changes, see if any of the solo phrases fit new keys
        if shuffled == False:
            temp_phrases = dict(phrases)
            for key in temp_phrases:
                if len(phrases[key]) == 1:
                    print("Finding match for " + str(phrases[key]))
                    for word in nltk.word_tokenize(phrases[key][0]):
                        print("  Checking " + word)
                        if word in phrases and word != key:
                            print("      Found word" )
                            phrases[word].append(phrases[key][0])
                            phrases.pop(key)
                            shuffled = True
                            break
        
        print("\n")
        for key in phrases:
            print(key + " : " + str(phrases[key]))
        print("\n")
                        
    return phrases