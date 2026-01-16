"""
NLTK-based vocabulary helper for scanners.
Replaces hardcoded pattern lists with linguistic analysis.
"""

from typing import List, Set, Optional
import nltk
from nltk.corpus import wordnet as wn
from nltk import pos_tag, word_tokenize

# Download required NLTK data if not already present
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet', quiet=True)

try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab', quiet=True)

try:
    nltk.data.find('taggers/averaged_perceptron_tagger_eng')
except LookupError:
    nltk.download('averaged_perceptron_tagger_eng', quiet=True)


class VocabularyHelper:
    """Helper class for linguistic analysis using NLTK."""
    
    # Agent noun suffixes (morphological patterns)
    AGENT_SUFFIXES = ['er', 'or', 'ar', 'ant', 'ent']
    
    # Gerund suffix
    GERUND_SUFFIX = 'ing'
    
    @staticmethod
    def is_verb(word: str) -> bool:
        """Check if word can function as a verb using WordNet."""
        try:
            word_lower = word.lower()
            synsets = wn.synsets(word_lower, pos=wn.VERB)
            return len(synsets) > 0
        except Exception:
            return False
    
    @staticmethod
    def is_noun(word: str) -> bool:
        """Check if word can function as a noun using WordNet."""
        try:
            word_lower = word.lower()
            synsets = wn.synsets(word_lower, pos=wn.NOUN)
            return len(synsets) > 0
        except Exception:
            return False
    
    @staticmethod
    def is_agent_noun(word: str) -> tuple[bool, Optional[str], Optional[str]]:
        """
        Check if word is an agent noun (doer of action).
        Returns: (is_agent, base_verb, suffix) or (False, None, None)
        
        Examples:
            'Manager' -> (True, 'manage', 'er')
            'Processor' -> (True, 'process', 'or')
            'Portfolio' -> (False, None, None)
        """
        word_lower = word.lower()
        
        for suffix in VocabularyHelper.AGENT_SUFFIXES:
            if word_lower.endswith(suffix) and len(word_lower) > len(suffix) + 2:
                base = word_lower[:-len(suffix)]
                
                # Check if base is a verb
                if VocabularyHelper.is_verb(base):
                    return (True, base, suffix)
                
                # Check common irregular forms
                # manage -> manager, coordinate -> coordinator
                if suffix == 'er' or suffix == 'or':
                    # Try adding 'e' back
                    base_with_e = base + 'e'
                    if VocabularyHelper.is_verb(base_with_e):
                        return (True, base_with_e, suffix)
        
        return (False, None, None)
    
    @staticmethod
    def is_gerund(word: str) -> tuple[bool, Optional[str]]:
        """
        Check if word is a gerund (verb + ing).
        Returns: (is_gerund, base_verb) or (False, None)
        
        Examples:
            'Loading' -> (True, 'load')
            'Running' -> (True, 'run')
            'Thing' -> (False, None)
        """
        word_lower = word.lower()
        
        if not word_lower.endswith(VocabularyHelper.GERUND_SUFFIX):
            return (False, None)
        
        if len(word_lower) <= len(VocabularyHelper.GERUND_SUFFIX) + 2:
            return (False, None)
        
        base = word_lower[:-len(VocabularyHelper.GERUND_SUFFIX)]
        
        # Check if base is a verb
        if VocabularyHelper.is_verb(base):
            return (True, base)
        
        # Check if base + 'e' is a verb (e.g., 'making' -> 'make')
        base_with_e = base + 'e'
        if VocabularyHelper.is_verb(base_with_e):
            return (True, base_with_e)
        
        # Check if we need to double the last letter (e.g., 'running' -> 'run')
        if len(base) > 1 and base[-1] == base[-2]:
            base_single = base[:-1]
            if VocabularyHelper.is_verb(base_single):
                return (True, base_single)
        
        return (False, None)
    
    @staticmethod
    def get_pos_tags(text: str) -> List[tuple[str, str]]:
        """Get part-of-speech tags for text."""
        try:
            tokens = word_tokenize(text)
            tokens = [t for t in tokens if t.isalnum() or any(c.isalnum() for c in t)]
            return pos_tag(tokens)
        except Exception:
            return []
    
    @staticmethod
    def is_verb_tag(tag: str) -> bool:
        """Check if POS tag indicates a verb."""
        verb_tags = ['VB', 'VBP', 'VBZ', 'VBD', 'VBG', 'VBN']
        return tag in verb_tags
    
    @staticmethod
    def is_noun_tag(tag: str) -> bool:
        """Check if POS tag indicates a noun."""
        noun_tags = ['NN', 'NNS', 'NNP', 'NNPS']
        return tag in noun_tags
    
    @staticmethod
    def is_proper_noun_tag(tag: str) -> bool:
        """Check if POS tag indicates a proper noun."""
        proper_noun_tags = ['NNP', 'NNPS']
        return tag in proper_noun_tags
    
    @staticmethod
    def is_actor_or_role(word: str) -> bool:
        """
        Check if word represents an actor or role (person, system, agent).
        Uses WordNet to check if word is a hyponym of 'person' or 'system'.
        
        Examples:
            'customer' -> True (person who buys)
            'user' -> True (person who uses)
            'developer' -> True (person who develops)
            'system' -> True (computing system)
            'api' -> True (system interface)
            'order' -> False (not a person/system)
        """
        try:
            word_lower = word.lower()
            
            # Get all synsets for the word
            synsets = wn.synsets(word_lower)
            
            if not synsets:
                return False
            
            # Get hypernym paths for all synsets
            for synset in synsets:
                # Get all hypernyms (parent concepts)
                hypernyms = set()
                for path in synset.hypernym_paths():
                    hypernyms.update(path)
                
                # Check if any hypernym is 'person', 'user', 'system', or 'agent'
                for hypernym in hypernyms:
                    name = hypernym.name().split('.')[0]
                    if name in ['person', 'user', 'system', 'agent', 'entity', 'causal_agent']:
                        return True
            
            return False
        except Exception:
            return False
        

