#
# Vladimir Kasatkin. April, 2015
#
# Run the 'build.py' script after doing "python manage.py collectstatic" 
#
# all folders must bu pointed form this config-file, e.g:
#
# - base_folder/
# |---config.py
# |---dev_templates/
# |---templates/

# Django's standart folder-style
SOURCE_DIRS = [
	"dev_templates/",
]

# results will be saved here
TARGET_DIR = "templates/" 

# all files that have [[[ "file_name.html" ]]] - include tag OR must be in target dir 
TARGET_FILES = [
	'base.html', 
	'core__ask.html', 
	'core__by_tag.html', 
	'core__index.html', 
	'core__question_page.html', 
	'user_profile__base.html', 
	'user_profile__login.html', 
	'user_profile__register.html', 
	'user_profile__setting.html',
	'404.html'
]
