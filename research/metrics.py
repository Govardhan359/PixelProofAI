from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, roc_auc_score

def compute_metrics(y_true, y_pred, y_scores=None):
    """
    Compute binary classification metrics.
    y_true: list of True (artificial), False (human)
    y_pred: list of True (artificial), False (human)
    y_scores: list of probability scores for 'artificial' class
    """
    metrics = {
        'total_samples': len(y_true),
        'accuracy': None,
        'precision': None,
        'recall': None,
        'f1_score': None,
        'roc_auc': None,
        'confusion_matrix': None,
    }
    
    if len(y_true) == 0:
        return metrics
        
    metrics['accuracy'] = accuracy_score(y_true, y_pred)
    metrics['precision'] = precision_score(y_true, y_pred, zero_division=0)
    metrics['recall'] = recall_score(y_true, y_pred, zero_division=0)
    metrics['f1_score'] = f1_score(y_true, y_pred, zero_division=0)
    
    cm = confusion_matrix(y_true, y_pred, labels=[False, True])
    metrics['confusion_matrix'] = {
        'tn': int(cm[0, 0]),
        'fp': int(cm[0, 1]),
        'fn': int(cm[1, 0]),
        'tp': int(cm[1, 1])
    }
    
    if y_scores is not None and len(set(y_true)) > 1:
        try:
            metrics['roc_auc'] = roc_auc_score(y_true, y_scores)
        except ValueError:
            pass
            
    return metrics
