from trello import TrelloClient
from datetime import datetime as tm


lists = { #for you need get your's list_id, this is mine list_id
    'need': '60cb65d0e2ec3e1d87e13b64',
    'work': '60cb65d0e2ec3e1d87e13b65',
    'arch': '60cb65d0e2ec3e1d87e13b66',
}
#            api_key                                            api_secret
tr = ['093d27453e811bf60ec06e5184b55550', '05902ff2287815e9e16ea826e6391afcf462ab4b294d1f67828457e5bbfa9f36']

client = TrelloClient(
    api_key=tr[0],
    api_secret=tr[1],
)

class MyTrello:

    def __init__(self):
        self.client = TrelloClient(
            api_key=tr[0],
            api_secret=tr[1],
        )
        self.member = self.client.get_member('60cb377c38b5d92176d8a789')

    def ad_memb(self, note, card):
        s = self.client.get_list(lists[card]).list_cards()
        for card in s:
            if card.name == note:
                card.add_member(self.member)

    def create_note(self, text, time):
        if time != '-':
            try:
                time_r = tm.strptime(time, "%d.%m.%y %H:%M")  # ("time" "time_r" "text"  "content");
            except:
                try:
                    time_r = tm.strptime(time, "%H:%M %d.%m.%y")
                except:
                    pass

            time_r = time.replace(hour=int(time.hour)-7)

            self.client.get_list(lists['need']).add_card(text, due=time_r.isoformat())
            self.ad_memb(text, 'need')

        else:
            self.client.get_list(lists['work']).add_card(text)
            self.ad_memb(text, 'work')



    def uptime(self, note, hours=3):
        s = self.client.get_list(lists['need']).list_cards()
        for card in s:
            if card.name == note:
                old_t = card.due
                old_t = tm.strptime(old_t, '%Y-%m-%dT%H:%M:00.000Z')  # "%H:%M %d.%m.%y"
                new_time = old_t.hour + hours
                new_day = new_time // 24
                new_hour = new_time % 24
                new_t = old_t.replace(hour=new_hour, day=old_t.day + new_day)
                card.set_due(new_t)

    def comleter(self, note):
        s = self.client.get_list(lists['need']).list_cards()
        for card in s:
            if card.name == note:
                card.set_due_complete()
                card.change_list(lists['arch'])
                card.delete()

        s = self.client.get_list(lists['work']).list_cards()
        for card in s:
            if card.name == note:
                card.set_due_complete()
                card.change_list(lists['arch'])
                card.delete()

    def get_notes(self):
        need_ = []
        work_ = []
        need = self.client.get_list(lists['need']).list_cards()
        work = self.client.get_list(lists['work']).list_cards()
        for i in need:
            try:
                d = tm.strptime(i.due, '%Y-%m-%dT%H:%M:%S.%fZ')
                new_time = d.hour + 3
                new_day = new_time // 24
                new_hour = new_time % 24
                time = d.replace(hour=new_hour, day=d.day + new_day)
                need_.append([i.name, f'{tm.strftime(time, "%d.%m.%y")} в {tm.strftime(time, "%H:%M")}'])
            except Exception as er:
                print(er)
                need_.append([i.name,])
        for i in work:
            work_.append([i.name])
        return([need_, work_])


if __name__ == "__main__":
    t = MyTrello()
    s = t.get_notes()
    print(s)