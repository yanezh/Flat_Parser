import os
import csv


class FlatsManager:

    def __init__(self, file_name, telegram_bot):
        self.data = {}
        self.file_name = file_name
        self.telegram_bot = telegram_bot
        self._read()

    def _read(self):
        if os.path.exists(self.file_name):
            with open(self.file_name, 'r') as file:
                csv_reader = csv.reader(file, delimiter=',')
                for row in csv_reader:
                    flat = {'price_usd': float(row[1]), 'last_update': row[2]}
                    self.data[row[0]] = flat

    def _save(self):
        with open(self.file_name, 'w', newline='') as file:
            writer = csv.writer(file, delimiter=',')
            for key in self.data:
                row = [key, self.data[key]['price_usd'], self.data[key]['last_update']]
                writer.writerow(row)
        print("Saved")

    def update(self, new_flats):
        changed = False
        for new_flat in new_flats:
            if new_flat['id'] not in self.data:
                self._add_flat(new_flat)
                changed = True
            elif new_flat['last_update'] != self.data[new_flat['id']]['last_update']:
                self._update_flat(new_flat)
                changed = True
        if changed:
            self._save()

    def _add_flat(self, flat):
        new_flat_dict = {'price_usd': flat['price_usd'], 'last_update': flat['last_update']}
        self.data[flat['id']] = new_flat_dict
        message = f"*Новая квартира!*\n*Адрес*: {flat['address']}\n*Цена*: {int(flat['price_usd'])}$\n" \
                  f"*Фото*: [{flat['photo']}]\n*Ссылка*: [{flat['url']}]"
        self._notify(message)

    def _update_flat(self, flat):
        flat_old = self.data[flat['id']]
        if flat_old['price_usd'] != flat['price_usd']:
            message = f"*Старая квартира обновлена!* Цена изменилась.\n*Адрес*: {flat['address']}\n" \
                      f"*Цена*: {int(flat_old['price_usd'])}$->{int(flat['price_usd'])}$\n*Фото*: [{flat['photo']}]\n" \
                      f"Ссылка: [{flat['url']}]"
        else:
            message = f"*Старая квартира обновлена!*\n*Адрес*: {flat['address']}\n" \
                      f"*Цена*: {int(flat['price_usd'])}$\n*Фото*: [{flat['photo']}]\n*Ссылка*: [{flat['url']}]"
        flat_old['price_usd'] = flat['price_usd']
        flat_old['last_update'] = flat['last_update']
        self._notify(message)

    def _notify(self, message):
        self.telegram_bot.send_message(message)
