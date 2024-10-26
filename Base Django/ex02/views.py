import logging
import os
from django.shortcuts import render, redirect
from django.conf import settings

from .forms import TextForm


def index(request):
  if not os.path.exists(settings.HISTORY_LOG_FILE):
    open(settings.HISTORY_LOG_FILE, 'a')

  logging.config.dictConfig(settings.LOGGING)

  logger = logging.getLogger('history')

  if request.method == 'POST':
    form = TextForm(request.POST)
    if form.is_valid():
      logger.info(form.cleaned_data['entry'])
      return redirect('/ex02')

  else:
    form = TextForm()

  try:
    with open(settings.HISTORY_LOG_FILE, 'r') as f:
      entries = [line.strip() for line in f.readlines()]

      formatted_entries = []
      for entry in entries:
          parts = entry.split(' ', 2)  # Split on the second space
          if len(parts) >= 3:
            timestamp = f"{parts[0]} {parts[1]}"  # Combine the first two parts as the timestamp
            message = parts[2]  # The rest is the message
            formatted_entries.append((timestamp, message))
  except:
    formatted_entries = []

  return render(request, 'ex02/text-form.html', {'form': form, 'entries': formatted_entries})
