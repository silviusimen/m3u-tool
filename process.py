import os
import time
import json
import logging

class AppUtil:
    def strtobool(val):
            val = val.lower()
            if val in ('y', 'yes', 't', 'true', 'on', '1'):
                return True
            elif val in ('n', 'no', 'f', 'false', 'off', '0'):
                return False
            else:
                raise ValueError("invalid truth value %r" % (val,))

    def tobool(val):
        if isinstance(val, str):
            return AppUtil.strtobool(val)
        elif isinstance(val, int):
            return bool(val)
        elif isinstance(val, bool):
            return val
        else:
            return AppUtil.strtobool(str(val))
    
    def toint(val):
        return int(val)

    def get_operating_parameters():
        global PANEL_FILE
        global PANEL_FILTER_FILE
        global OUT_M3U_FILE
        global LOG_TO_FILE_ENABLED

        PANEL_FILE = os.environ.get('PANEL_FILE', 'KY-panel.json')
        PANEL_FILTER_FILE = os.environ.get('PANEL_FILTER_FILE', 'KY-filter_all.json')
        OUT_M3U_FILE = os.environ.get('OUT_M3U_FILE', 'ky-filter-1.m3u')
        LOG_TO_FILE_ENABLED = AppUtil.tobool(os.environ.get('LOG_TO_FILE_ENABLED', False))

    def log_setup():
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        handlers=[console_handler]
        if LOG_TO_FILE_ENABLED:
            file_handler = logging.FileHandler('process_log_{}.log'.format(time.time()))
            file_handler.setLevel(logging.WARN)
            handlers.append(file_handler)
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', handlers=handlers)

    def on_start(self):
        AppUtil.get_operating_parameters()
        AppUtil.log_setup()
        logging.debug('Starting')
        self.time_start = time.time()

    def on_stop(self):
        time_end = time.time()
        total_time = time_end - self.time_start
        logging.debug('Processing time: {}'.format(total_time))
        logging.debug('Completed')

class JSON:
    def json_load(filename:str):
        with open(filename) as infile:
          data = json.load(infile)
        return data
    def json_write(filename:str, data: dict):
        with open(filename, "w") as outfile:
          json_object = json.dumps(data, indent=4)
          outfile.write(json_object)

class M3U:
  def render_m3u_entry_extinf(entry: dict):
    buffer = "#EXTINF:-1 "
    buffer += 'tvg-id="' + entry['stream_id'] +'" '
    buffer += 'tvg-name="' + entry['name'] + '" '
    buffer += 'tvg-logo="' + entry['stream_icon'] + '" '
    buffer += 'group-title="' + entry['category_name'] +'"'
    buffer += ',' + entry['name']
    return buffer

  def render_m3u_entry_url(base_url:str, entry: dict):
    id = entry['stream_id']
    return base_url + "/" + id + ".ts"

  def render_m3u(m3u_entries: list, filename: str, base_url: str):
    with open(filename, "w") as outfile:
      outfile.write("#EXTM3U" + '\n')
      for entry in m3u_entries:
        outfile.write(M3U.render_m3u_entry_extinf(entry) + '\n')
        outfile.write(M3U.render_m3u_entry_url(base_url, entry) + '\n')

class PANEL:
  def get_active_categories(panel_data, filter_definition):
    all_categories = panel_data['categories']['live']
    included_categories = frozenset(filter_definition['included_categories'])
    categories = [cat for cat in all_categories if cat['category_name'] in included_categories]
    return categories

  def categories_list_to_dict_by_id(categories: list):
    dict_cat = dict()
    for c in categories:
      dict_cat[c['category_id']] = c
    return dict_cat

  def filter_channels_by_category(channels: dict, categories: dict):
    return [chanel for id, chanel in channels.items() if chanel['category_id'] in categories ]

  def get_base_stream_url(panel_data: dict):
    base_url = panel_data['server_info']['server_protocol']
    base_url += "://"
    base_url += panel_data['server_info']['url']
    base_url += ":"
    base_url += panel_data['server_info']['port']
    base_url += "/"
    base_url += panel_data['user_info']['username']
    base_url += "/"
    base_url += panel_data['user_info']['password']
    return base_url


class KY:
    def generate_list_of_all_categories_to_file(data: dict, type: str, filename: str):
      file_contents = { 'all_categories' : [ x['category_name'] for x in data['categories'][type] ] } 
      JSON.json_write(filename, file_contents)

    def process():
      logging.debug('Loading filter file {} '.format(PANEL_FILTER_FILE))
      filter_definition = JSON.json_load(PANEL_FILTER_FILE)
      logging.debug('Loading filter file {} complete'.format(PANEL_FILTER_FILE))

      logging.debug('Loading panel file {} '.format(PANEL_FILE))
      panel_data = JSON.json_load(PANEL_FILE)
      logging.debug('Loading panel file {} complete'.format(PANEL_FILE))

      logging.debug('Processing')
      categories = PANEL.get_active_categories(panel_data, filter_definition)
      categories_dict = PANEL.categories_list_to_dict_by_id(categories)
      channels = PANEL.filter_channels_by_category(panel_data['available_channels'], categories_dict)
      base_url = PANEL.get_base_stream_url(panel_data)
      logging.debug('Writing results to file {}'.format(OUT_M3U_FILE))
      M3U.render_m3u(channels, OUT_M3U_FILE, base_url)

if __name__ == '__main__':
    app = AppUtil()
    app.on_start()
    KY.process();
    app.on_stop()
