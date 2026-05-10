"""Machine Learning Model for JavaScript Code Analysis"""

import numpy as np
import tensorflow as tf
from tensorflow import keras
from typing import Dict, List, Tuple, Optional
from pathlib import Path
from loguru import logger


class JSCodeClassifier:
    """TensorFlow model for classifying JavaScript code quality"""
    
    def __init__(self, input_features: int = 50, output_classes: int = 5):
        """
        Initialize the model
        
        Args:
            input_features: Number of input features from JS analyzer
            output_classes: Number of classification classes (poor, fair, good, excellent, secure)
        """
        self.input_features = input_features
        self.output_classes = output_classes
        self.model = None
        self.history = None
        self.scaler = None
    
    def build_model(self) -> keras.Model:
        """Build neural network architecture"""
        model = keras.Sequential([
            keras.layers.Dense(128, activation='relu', input_shape=(self.input_features,)),
            keras.layers.BatchNormalization(),
            keras.layers.Dropout(0.3),
            
            keras.layers.Dense(64, activation='relu'),
            keras.layers.BatchNormalization(),
            keras.layers.Dropout(0.3),
            
            keras.layers.Dense(32, activation='relu'),
            keras.layers.BatchNormalization(),
            keras.layers.Dropout(0.2),
            
            keras.layers.Dense(16, activation='relu'),
            keras.layers.Dropout(0.2),
            
            keras.layers.Dense(self.output_classes, activation='softmax')
        ])
        
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='categorical_crossentropy',
            metrics=['accuracy', keras.metrics.Precision(), keras.metrics.Recall()]
        )
        
        self.model = model
        return model
    
    def train(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: Optional[np.ndarray] = None,
        y_val: Optional[np.ndarray] = None,
        epochs: int = 50,
        batch_size: int = 32,
        verbose: int = 1
    ) -> keras.callbacks.History:
        """
        Train the model
        
        Args:
            X_train: Training features
            y_train: Training labels
            X_val: Validation features
            y_val: Validation labels
            epochs: Number of training epochs
            batch_size: Batch size
            verbose: Verbosity level
            
        Returns:
            Training history
        """
        if self.model is None:
            self.build_model()
        
        validation_data = None
        if X_val is not None and y_val is not None:
            validation_data = (X_val, y_val)
        
        callbacks = [
            keras.callbacks.EarlyStopping(
                monitor='val_loss' if validation_data else 'loss',
                patience=10,
                restore_best_weights=True
            ),
            keras.callbacks.ReduceLROnPlateau(
                monitor='val_loss' if validation_data else 'loss',
                factor=0.5,
                patience=5,
                min_lr=0.00001
            )
        ]
        
        self.history = self.model.fit(
            X_train, y_train,
            validation_data=validation_data,
            epochs=epochs,
            batch_size=batch_size,
            callbacks=callbacks,
            verbose=verbose
        )
        
        return self.history
    
    def predict(self, X: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Make predictions
        
        Args:
            X: Features to predict on
            
        Returns:
            Predictions and confidence scores
        """
        if self.model is None:
            raise ValueError("Model not trained. Call build_model() and train() first.")
        
        predictions = self.model.predict(X)
        class_labels = np.argmax(predictions, axis=1)
        confidence_scores = np.max(predictions, axis=1)
        
        return class_labels, confidence_scores
    
    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray) -> Dict:
        """
        Evaluate model on test data
        
        Args:
            X_test: Test features
            y_test: Test labels
            
        Returns:
            Evaluation metrics
        """
        if self.model is None:
            raise ValueError("Model not trained.")
        
        loss, accuracy, precision, recall = self.model.evaluate(X_test, y_test, verbose=0)
        
        return {
            "loss": float(loss),
            "accuracy": float(accuracy),
            "precision": float(precision),
            "recall": float(recall),
            "f1_score": 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        }
    
    def save_model(self, path: str):
        """Save model to disk"""
        if self.model is None:
            raise ValueError("No model to save.")
        
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.model.save(path)
        logger.info(f"Model saved to {path}")
    
    def load_model(self, path: str):
        """Load model from disk"""
        self.model = keras.models.load_model(path)
        logger.info(f"Model loaded from {path}")
    
    def get_feature_importance(self) -> Dict[str, float]:
        """Get feature importance (for interpretation)"""
        if self.model is None or len(self.model.layers) == 0:
            return {}
        
        # Get weights from first dense layer
        weights = self.model.layers[0].get_weights()[0]
        importance = np.abs(weights).mean(axis=1)
        
        feature_names = [f"feature_{i}" for i in range(len(importance))]
        importance_dict = {name: float(imp) for name, imp in zip(feature_names, importance)}
        
        return importance_dict


class FeatureExtractor:
    """Extract ML features from JavaScript analysis results"""
    
    @staticmethod
    def extract_features(analysis_result: Dict) -> np.ndarray:
        """
        Convert analysis result to feature vector
        
        Args:
            analysis_result: Output from JavaScriptAnalyzer
            
        Returns:
            Feature vector as numpy array
        """
        features = []
        
        # Metrics
        metrics = analysis_result.get("metrics", {})
        features.extend([
            metrics.get("total_lines", 0),
            metrics.get("non_empty_lines", 0),
            metrics.get("comment_lines", 0),
            metrics.get("characters", 0),
            metrics.get("imports", 0),
            metrics.get("exports", 0),
            metrics.get("functions", 0),
            metrics.get("classes", 0),
            metrics.get("async_functions", 0),
        ])
        
        # Complexity
        complexity = analysis_result.get("complexity", {})
        features.extend([
            complexity.get("conditional", 0),
            complexity.get("loop", 0),
            complexity.get("function", 0),
            complexity.get("async", 0),
            complexity.get("error_handling", 0),
            complexity.get("security_issue", 0),
            complexity.get("api_call", 0),
            complexity.get("lazy_loading", 0),
            complexity.get("cyclomatic_estimate", 0),
        ])
        
        # Security
        security = analysis_result.get("security", {})
        features.extend([
            security.get("eval_usage", 0),
            security.get("innerHTML", 0),
            security.get("document_write", 0),
            security.get("unsafe_timing", 0),
            security.get("missing_validation", 0),
            security.get("hardcoded_secrets", 0),
            security.get("sql_injection", 0),
            security.get("xss_potential", 0),
            security.get("risk_score", 0),
            1 if security.get("is_vulnerable", False) else 0,
        ])
        
        # Patterns (convert to binary/count)
        patterns = analysis_result.get("patterns", {})
        features.extend([
            1 if patterns.get("uses_react", False) else 0,
            1 if patterns.get("uses_async", False) else 0,
            1 if patterns.get("uses_arrow_functions", False) else 0,
            1 if patterns.get("uses_classes", False) else 0,
            1 if patterns.get("uses_destructuring", False) else 0,
            1 if patterns.get("uses_spread_operator", False) else 0,
            1 if patterns.get("uses_template_literals", False) else 0,
            1 if patterns.get("has_tests", False) else 0,
            1 if patterns.get("has_jsdoc", False) else 0,
        ])
        
        # Ensure we have correct number of features
        while len(features) < 50:
            features.append(0)
        
        return np.array(features[:50], dtype=np.float32)


class ModelEnsemble:
    """Ensemble of models for robust predictions"""
    
    def __init__(self, num_models: int = 3):
        self.models = [JSCodeClassifier() for _ in range(num_models)]
        self.num_models = num_models
    
    def train_ensemble(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: Optional[np.ndarray] = None,
        y_val: Optional[np.ndarray] = None,
        epochs: int = 50
    ):
        """Train all models in ensemble"""
        for i, model in enumerate(self.models):
            logger.info(f"Training model {i+1}/{self.num_models}")
            model.build_model()
            model.train(X_train, y_train, X_val, y_val, epochs=epochs, verbose=0)
    
    def predict_ensemble(self, X: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Make ensemble predictions (voting)
        
        Args:
            X: Features to predict
            
        Returns:
            Ensemble predictions and average confidence
        """
        all_predictions = []
        all_confidences = []
        
        for model in self.models:
            preds, confs = model.predict(X)
            all_predictions.append(preds)
            all_confidences.append(confs)
        
        # Majority voting
        ensemble_preds = np.apply_along_axis(
            lambda x: np.bincount(x).argmax(),
            axis=0,
            arr=np.array(all_predictions)
        )
        
        # Average confidence
        avg_confidence = np.mean(all_confidences, axis=0)
        
        return ensemble_preds, avg_confidence
