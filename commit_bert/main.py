from functions import predict_message

test_diff = """--- test1.py	2022-03-27 13:42:33.641409462 +0000
+++ test2.py	2022-03-27 13:42:25.471839267 +0000
@@ -5,3 +5,7 @@
    return np.sin(x) + x + x * np.sin(x)
 
 x = np.linspace(-10, 10, 100)
+
+plt.plot(x, f(x), color='blue')
+
+plt.show()
\ No newline at end of file"""

result = predict_message(test_diff)
print('\ngit commit -m \''+ result +'\'')