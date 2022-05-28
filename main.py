from tkinter import *
import sqlite3

root = Tk()
root.iconbitmap('computer.ico')
# create db
conn = sqlite3.connect('address_book.db')
# cursor object
cur = conn.cursor()
# query db
cur.execute('''CREATE TABLE IF NOT EXISTS addresses (
            first_name text,
            last_name text,
            address text,
            city text,
            state text,
            zipcode integer)
            ''')
# commit changes
conn.commit()
# close
cur.close()

query_label = Label(root)
query_label.grid(row=12, column=0, columnspan=2, ipady=10)


def query():
    global query_label
    # create db
    conn = sqlite3.connect('address_book.db')
    # cursor object
    cur = conn.cursor()
    # query db
    # , oid represents primary key id
    cur.execute('SELECT *, oid FROM addresses')
    # we can .fetchone() or .fetchmany(30) etc....
    records = cur.fetchall()
    # print(records)
    print_records = ''
    # we create a for loop to iterate through the entries.
    for record in records:
        print_records += str(record[6]) + ' ' + str(record[0]) + ' ' + str(record[1]) + ' ' + str(record[2]) + '\n'
    query_label.grid_forget()
    query_label = Label(root, text=print_records)
    query_label.grid(row=12, column=0, columnspan=2, ipady=10)
    # print(print_records)

    # commit changes
    conn.commit()
    # close connection
    conn.close()


# wrapper function for submit button
def submit():
    global query_label
    if len(f_name.get()) == 0 or len(l_name.get()) == 0 or len(address.get()) == 0 or len(city.get()) == 0 or len(state.get()) == 0 or len(
            zipcode.get()) == 0:
        query_label.grid_forget()
        query_label = Label(root, text='please fill the required entries...')
        query_label.grid(row=12, column=0, columnspan=2, ipady=10)
    else:
        # create db
        conn = sqlite3.connect('address_book.db')
        # cursor object
        cur = conn.cursor()
        # insert into db table
        # the entries used as key pair here could be named anything of your choice in string format.
        cur.execute('INSERT INTO addresses VALUES (:f_name, :l_name, :address, :city, :state, :zipcode)',
                    {
                        'f_name': f_name.get(),
                        'l_name': l_name.get(),
                        'address': address.get(),
                        'city': city.get(),
                        'state': state.get(),
                        'zipcode': zipcode.get(),
                    })
        # commit changes
        conn.commit()
        # close connection
        conn.close()

    # clear the text field entry.
    f_name.delete(0, END)
    l_name.delete(0, END)
    address.delete(0, END)
    city.delete(0, END)
    state.delete(0, END)
    zipcode.delete(0, END)


# delete a record
def delete():
    # create db
    conn = sqlite3.connect('address_book.db')
    # cursor object
    cur = conn.cursor()
    # delete a record
    cur.execute('DELETE FROM addresses WHERE oid=' + delete_box.get())
    # commit changes
    conn.commit()
    # close connection
    conn.close()


# wrapper function to edit records.
def edit():
    global layer_2
    layer_2 = Tk()
    layer_2.iconbitmap('computer.ico')
    layer_2.title('Update a record')
    layer_2.geometry('280x290')

    # create db
    conn = sqlite3.connect('address_book.db')
    # cursor object
    cur = conn.cursor()
    # query db
    record_id = delete_box.get()
    # , oid represents primary key id
    cur.execute('SELECT * FROM addresses WHERE oid=' + record_id)
    record = cur.fetchall()

    # create global variables for text box names.
    global f_name_editor
    global l_name_editor
    global address_editor
    global city_editor
    global state_editor
    global zipcode_editor
    # entries
    f_name_editor = Entry(layer_2, width=30)
    l_name_editor = Entry(layer_2, width=30)
    address_editor = Entry(layer_2, width=30)
    city_editor = Entry(layer_2, width=30)
    state_editor = Entry(layer_2, width=30)
    zipcode_editor = Entry(layer_2, width=30)

    f_name_editor.grid(row=0, column=1, pady=(10, 0))
    l_name_editor.grid(row=1, column=1)
    address_editor.grid(row=2, column=1)
    city_editor.grid(row=3, column=1)
    state_editor.grid(row=4, column=1)
    zipcode_editor.grid(row=5, column=1)

    # entries label
    f_name_label = Label(layer_2, text='First Name')
    l_name_label = Label(layer_2, text='Last Name')
    address_label = Label(layer_2, text='Address')
    city_label = Label(layer_2, text='City')
    state_label = Label(layer_2, text='State')
    zipcode_label = Label(layer_2, text='Zipcode')

    f_name_label.grid(row=0, column=0, pady=(10, 0))
    l_name_label.grid(row=1, column=0)
    address_label.grid(row=2, column=0)
    city_label.grid(row=3, column=0)
    state_label.grid(row=4, column=0)
    zipcode_label.grid(row=5, column=0)

    # loop through results
    for rec in record:
        f_name_editor.insert(0, rec[0])
        l_name_editor.insert(0, rec[1])
        address_editor.insert(0, rec[2])
        city_editor.insert(0, rec[3])
        state_editor.insert(0, rec[4])
        zipcode_editor.insert(0, rec[5])

    # save button to save records.
    submit_button = Button(layer_2, text='Update Records', command=update)
    submit_button.grid(row=6, column=0, columnspan=2, ipadx=80)

    layer_2.mainloop()


def update():
    # create db
    conn = sqlite3.connect('address_book.db')
    # cursor object
    cur = conn.cursor()
    record_id = delete_box.get()
    # code to update the records.
    cur.execute('''UPDATE addresses SET
    first_name = :first,
    last_name = :last,
    address = :address,
    city = :city,
    state = :state,
    zipcode = :zipcode
    WHERE oid = :oid''',
                {'first': f_name_editor.get(),
                 'last': l_name_editor.get(),
                 'address': address_editor.get(),
                 'city': city_editor.get(),
                 'state': state_editor.get(),
                 'zipcode': zipcode_editor.get(),
                 'oid': record_id
                 })
    cur.execute('SELECT *, oid FROM addresses')
    # we can .fetchone() or .fetchmany(30) etc....
    records = cur.fetchall()
    conn.commit()
    conn.close()
    # print(records)
    print_records = ''
    # we create a for loop to iterate through the entries.
    for record in records:
        print_records += str(record[6]) + ' ' + str(record[1]) + ' ' + str(record[0]) + '\n'

    query_label = Label(layer_2, text=print_records)
    query_label.grid(row=7, column=0, columnspan=2, ipady=10)

    layer_2.destroy()


# entries
f_name = Entry(root, width=30)
l_name = Entry(root, width=30)
address = Entry(root, width=30)
city = Entry(root, width=30)
state = Entry(root, width=30)
zipcode = Entry(root, width=30)

f_name.grid(row=0, column=1, pady=(10, 0))
l_name.grid(row=1, column=1)
address.grid(row=2, column=1)
city.grid(row=3, column=1)
state.grid(row=4, column=1)
zipcode.grid(row=5, column=1)

# entries label
f_name_label = Label(root, text='First Name')
l_name_label = Label(root, text='Last Name')
address_label = Label(root, text='Address')
city_label = Label(root, text='City')
state_label = Label(root, text='State')
zipcode_label = Label(root, text='Zipcode')

f_name_label.grid(row=0, column=0, pady=(10, 0))
l_name_label.grid(row=1, column=0)
address_label.grid(row=2, column=0)
city_label.grid(row=3, column=0)
state_label.grid(row=4, column=0)
zipcode_label.grid(row=5, column=0)

# button
submit_button = Button(root, text='Submit Entries to Database', command=submit)
submit_button.grid(row=6, column=0, columnspan=2, ipadx=100)

# query button
submit_button = Button(root, text='Show Records', command=query)
submit_button.grid(row=7, column=0, columnspan=2, ipadx=133)

# delete_box
delete_box = Entry(root, width=30)
delete_box.grid(row=9, column=1)

delete_box_label = Label(root, text='Select ID')
delete_box_label.grid(row=9, column=0)

# delete button
delete_button = Button(root, text='Delete Record', command=delete)
delete_button.grid(row=10, column=0, columnspan=2, ipadx=133)

# create an update button
edit_button = Button(root, text='Edit Record', command=edit)
edit_button.grid(row=11, column=0, columnspan=2, pady=10, ipadx=140)

root.mainloop()
