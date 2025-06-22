with open('src/components/StartLineScanner.vue', 'r') as f: content = f.read()
content = content.replace('  // Tu można dodać toast notification', '  alert(`✅ SUKCES: ${message}`)')
