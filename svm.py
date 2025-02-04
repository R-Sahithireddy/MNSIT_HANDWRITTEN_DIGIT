import sys
import numpy as np
import pickle
import pandas as pd
from sklearn import model_selection, svm, preprocessing
from sklearn.metrics import accuracy_score, confusion_matrix
import matplotlib.pyplot as plt
from matplotlib import style

style.use("ggplot")

# Save all the print statements in a log file
old_stdout = sys.stdout
log_file = open("summary.log", "w")
sys.stdout = log_file

# Load MNIST data from CSV
print("\nLoading MNIST Data...")

print("\nLoading Training Data...")
train_data = pd.read_csv("C:\\Users\\SPN\\Desktop\\int\\mnist_train.csv")
train_img = train_data.drop("label", axis=1).values
train_labels = train_data["label"].values

print("\nLoading Testing Data...")
test_data = pd.read_csv("C:\\Users\\SPN\\Desktop\\int\\mnist_test.csv")
test_img = test_data.drop("label", axis=1).values
test_labels = test_data["label"].values

# Features
X = train_img

# Labels
y = train_labels

# Prepare Classifier Training and Testing Data
print("\nPreparing Classifier Training and Validation Data...")
X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=0.1)

# Pickle the classifier for future use
print("\nSVM Classifier with gamma = 0.1; Kernel = polynomial")
print("\nPickling the Classifier for Future Use...")
clf = svm.SVC(gamma=0.1, kernel="poly")
clf.fit(X_train, y_train)

with open("MNIST_SVM.pickle", "wb") as f:
    pickle.dump(clf, f)

pickle_in = open("MNIST_SVM.pickle", "rb")
clf = pickle.load(pickle_in)

print("\nCalculating Accuracy of trained Classifier...")
acc = clf.score(X_test, y_test)

print("\nMaking Predictions on Validation Data...")
y_pred = clf.predict(X_test)

print("\nCalculating Accuracy of Predictions...")
accuracy = accuracy_score(y_test, y_pred)

print("\nCreating Confusion Matrix...")
conf_mat = confusion_matrix(y_test, y_pred)

print("\nSVM Trained Classifier Accuracy: ", acc)
print("\nPredicted Values: ", y_pred)
print("\nAccuracy of Classifier on Validation Images: ", accuracy)
print("\nConfusion Matrix: \n", conf_mat)

# Plot confusion matrix data as a matrix
plt.matshow(conf_mat)
plt.title("Confusion Matrix for Validation Data")
plt.colorbar()
plt.ylabel("True label")
plt.xlabel("Predicted label")
plt.show()

print("\nMaking Predictions on Test Input Images...")
test_labels_pred = clf.predict(test_img)

print("\nCalculating Accuracy of Trained Classifier on Test Data...")
acc_test = accuracy_score(test_labels, test_labels_pred)

print("\nCreating Confusion Matrix for Test Data...")
conf_mat_test = confusion_matrix(test_labels, test_labels_pred)

print("\nPredicted Labels for Test Images: ", test_labels_pred)
print("\nAccuracy of Classifier on Test Images: ", acc_test)
print("\nConfusion Matrix for Test Data: \n", conf_mat_test)

# Plot confusion matrix for test data
plt.matshow(conf_mat_test)
plt.title("Confusion Matrix for Test Data")
plt.colorbar()
plt.ylabel("True label")
plt.xlabel("Predicted label")
plt.axis("off")
plt.show()

sys.stdout = old_stdout
log_file.close()

# Save results to CSV
results_df = pd.DataFrame(
    {"True Label": test_labels, "Predicted Label": test_labels_pred}
)
results_df.to_csv("svm_predictions.csv", index=False)

# Show the test images with original and predicted labels
a = np.random.randint(1, len(test_img), 15)
for i in a:
    two_d = (np.reshape(test_img[i], (28, 28)) * 255).astype(np.uint8)
    plt.title(
        "Original Label: {0}  Predicted Label: {1}".format(
            test_labels[i], test_labels_pred[i]
        )
    )
    plt.imshow(two_d, interpolation="nearest", cmap="gray")
    plt.show()
