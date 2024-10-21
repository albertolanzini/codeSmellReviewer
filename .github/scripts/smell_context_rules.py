SMELL_CONTEXT_RULES = {
    # Method-related smells
    "java:S1144": {  # Unused private method
        "scope": "method",
        "extra_context": {"above": 0, "below": 0, "needs_class_context": True},
        "description": "Unused private method"
    },
    "java:S1488": {  # Local variable could be final
        "scope": "variable",
        "extra_context": {"above": 2, "below": 3, "needs_class_context": False},
        "description": "Immutable variable"
    },
    "java:S138": {  # Method too long
        "scope": "method",
        "extra_context": {"above": 0, "below": 0, "needs_class_context": False},
        "description": "Method length"
    },
    "java:S1541": {  # Method complexity
        "scope": "method",
        "extra_context": {"above": 0, "below": 0, "needs_class_context": False},
        "description": "Method complexity"
    },
    
    # Class-related smells
    "java:S1200": {  # Class has too many methods
        "scope": "class",
        "extra_context": {"above": 0, "below": 0, "needs_full_class": True},
        "description": "Class size"
    },
    "java:S1448": {  # Class should be final
        "scope": "class",
        "extra_context": {"above": 0, "below": 0, "needs_class_signature": True},
        "description": "Class mutability"
    },
    
    # Code organization smells
    "java:S1199": {  # Nested code blocks
        "scope": "block",
        "extra_context": {"above": 3, "below": 3, "needs_method_context": True},
        "description": "Nested blocks"
    },
    "java:S1066": {  # Mergeable if statements
        "scope": "block",
        "extra_context": {"above": 2, "below": 2, "needs_method_context": True},
        "description": "Conditional statements"
    },
    
    # OOP smells
    "java:S1989": {  # God Class
        "scope": "class",
        "extra_context": {"above": 0, "below": 0, "needs_full_class": True},
        "description": "Class responsibilities"
    },
    "java:S1450": {  # Private field could be local variable
        "scope": "field",
        "extra_context": {"above": 1, "below": 1, "needs_class_context": True},
        "description": "Field scope"
    },
    
    # Default rule
    "default": {
        "scope": "block",
        "extra_context": {"above": 3, "below": 3, "needs_class_context": False},
        "description": "Code issue"
    }
}