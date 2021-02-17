from tkinter import *
import tkinter.messagebox as msgbox
import json
import numpy as np
import pickle
from columns_list import X_list


def predict_price(location, sqft, bath, bhk):
    load_model = pickle.load(open('banglore_home_prices_model.pickle', 'rb'))
    loc_index = X_list.index(location)
    x = np.zeros(len(X_list))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if loc_index >= 0:
        x[loc_index] = 1

    return load_model.predict([x])[0]


class callPrice(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1080x500")
        self.title("House Pricing Predictor")
        icon = PhotoImage(file='house.png')
        self.iconphoto(False, icon)

    def status(self):
        self.statusvar = StringVar()
        self.statusvar.set("Ready")
        self.statusbar = Label(self, textvar=self.statusvar, relief=SUNKEN, anchor='w')
        self.statusbar.pack(side=BOTTOM, fill=X)

    def menus(self):
        main_menu = Menu(root)
        file_menu = Menu(main_menu, tearoff=0)
        file_menu.add_command(label="Exit", command=root.destroy)
        about_menu = Menu(main_menu, tearoff=0)
        about_menu.add_command(label="About")
        root.config(menu=main_menu)
        main_menu.add_cascade(label="File", menu=file_menu)
        main_menu.add_cascade(label="Help", menu=about_menu)

    def body(self):
        f = open('area.json')
        data = json.load(f)

        title_label = Label(root, text="House Pricing Predictor", bg='#f1f1f1', fg='blue', pady=20,
                            font='Verdana 22 bold underline')
        title_label.place(x=400, y=25)

        f1 = Frame(root, bg='#f1f1f1')
        f1.place(x=100, y=150)

        scrollbar = Scrollbar(f1)
        scrollbar.pack(side=RIGHT, fill=BOTH)

        list_label = Label(root, text="Select Location:", font='arial 12 bold')
        list_label.place(x=100, y=120)

        i = 0
        self.list = Listbox(f1)
        self.list.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.list.yview)
        for area in data['area']:
            self.list.insert(i, area)
            i += 1

        self.list.pack(ipadx=25)

        sqrft_label = Label(root, text="Select Area(Square Feet):", font='arial 12 bold')
        sqrft_label.place(x=350, y=120)
        self.sqrft_value = StringVar()
        sqrft_entry = Entry(root, textvariable=self.sqrft_value)
        sqrft_entry.place(x=350, y=150)

        room_label = Label(root, text="Select No. of Rooms:", font='arial 12 bold')
        room_label.place(x=600, y=120)
        self.room_value = StringVar()
        room_entry = Entry(root, textvariable=self.room_value)
        room_entry.place(x=600, y=150)

        bathroom_label = Label(root, text="Select No. of Bathroom(s):", font='arial 12 bold')
        bathroom_label.place(x=800, y=120)
        self.bathroom_value = StringVar()
        bathroom_entry = Entry(root, textvariable=self.bathroom_value)
        bathroom_entry.place(x=800, y=150)

    def getAllValues(self):
        try:
            print('--- Try Starts ---')
            print(self.list.get(self.list.curselection()))
            print(self.sqrft_value.get())
            print(self.room_value.get())
            print(self.bathroom_value.get())
            print('---Try Ends---')
        except Exception:
            print('--- Exception Starts ---')
            msgbox.showinfo('Incomplete Data', 'Please Select any one of location in list')
            self.statusvar.set('No Location Selected - Please Select any one of location in list')
            print('--- Exception Ends ---')
        else:
            print('--- Else Starts ---')
            if self.sqrft_value.get() == '':
                print('No value for Area')
                msgbox.showinfo('Incomplete Data', 'Please Enter Area(Square Feet)')
                self.statusvar.set('Please Enter Area(Square Feet)')
            if self.room_value.get() == '':
                print('No value for Room')
                msgbox.showinfo('Incomplete Data', 'Please Enter No. of Rooms')
                self.statusvar.set('Please Enter No. of Rooms')
            if self.bathroom_value.get() == '':
                print('No value for Bathroom')
                msgbox.showinfo('Incomplete Data', 'Please Enter No. of Bathroom(s)')
                self.statusvar.set('Please Enter No. of Bathroom(s)')
            if self.sqrft_value.get() == '' or self.room_value.get() == '' or self.bathroom_value.get() == '':
                print('Do Not Call Model')
                self.statusvar.set('Cannot Process Due to Incomplete Data')
            else:
                location = self.list.get(self.list.curselection())
                sqft = self.sqrft_value.get()
                bath = self.bathroom_value.get()
                rooms = self.room_value.get()
                self.statusvar.set('Predicting Price')
                print('Call Model')
                price = round(predict_price(location, sqft, bath, rooms), 2)
                print(price)
                msgbox.showinfo('Price Predicted', f'Predicted Price is: {price}')
                self.statusvar.set(f'Predicted Price is: {price}')
                # print(predict_price('1st Phase JP Nagar', 1000, 2, 2))
            print('--- Else Ends ---')

    def callButton(self):
        button = Button(root, text="Predict Price", bg='orange', fg='white', pady=10, padx=10,
                        font="timesnewroman 12 bold",
                        command=self.getAllValues)
        button.place(x=500, y=350)


if __name__ == '__main__':
    root = callPrice()
    root.menus()
    root.body()
    root.callButton()
    root.status()
    root.mainloop()
