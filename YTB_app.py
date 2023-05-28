import subprocess
def install_libraries():
    try:
        subprocess.check_call(['pip', 'install', '-r', 'requirements.txt'])
        return print("Library installation successful!")
    except subprocess.CalledProcessError as e:
        return print("An error occurred while installing libraries:", e)

# Call the install_libraries() function to install the libraries
install_libraries()
command = "streamlit run YOUTUBE_STREAMLIT_app.py"
subprocess.Popen(['cmd', '/c', command])
subprocess.wait()
