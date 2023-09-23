from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import sys
import os

#login into cloudfirestore
# with service account
cred = credentials.Certificate("dbmanager-e2eff-firebase-adminsdk-qe0t9-82b8e9a916.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

#fixed layout
ws = Tk()
ws.geometry('600x600')
ws.title('Database Manager')
ws.configure(bg = 'white')
f = ("Times bold", 10)
t = ("Times bold", 13)

#index filter
frame = Frame(ws)
frame.grid()

valt = BooleanVar()
vals = BooleanVar()
vald = BooleanVar()
valh = BooleanVar()
valb = BooleanVar()
values = [valt, vals, vald, valh, valb]

def apply():
    #check which checkbutton is checked
    if(apply_price.get() or apply_quant.get()):
        try: 
            dell()
            getproducts(valt.get(), vals.get(), vald.get(), valh.get(), valb.get(), TRUE)
            quant_num.set(0)
            price_num.set(0.00)
            apply_cat.set(FALSE)
            apply_price.set(FALSE)
            apply_quant.set(FALSE)
            showchecks()
            valt.set(FALSE)
            vals.set(FALSE)
            vald.set(FALSE)
            valh.set(FALSE)
            valb.set(FALSE)
        except:
            messagebox.showerror("Error", "Invalid values")
    else:
        dell() #reset
        getproducts(valt.get(), vals.get(), vald.get(), valh.get(), valb.get(), TRUE)
        quant_num.set(0)
        price_num.set(0.00)
        apply_cat.set(FALSE)
        apply_price.set(FALSE)
        apply_quant.set(FALSE)
        showchecks()
        valt.set(FALSE)
        vals.set(FALSE)
        vald.set(FALSE)
        valh.set(FALSE)
        valb.set(FALSE)
      
def showchecks():
    if(apply_cat.get()):
        checkframe2.pack()
    else:
        checkframe2.pack_forget()
    if(apply_quant.get()):
        quantityframe.pack()
    else:
        quantityframe.pack_forget()
    if(apply_price.get()):
        priceframe.pack()
    else:
        priceframe.pack_forget()

fil = Label(frame, text = "Products Manager", font = t, width = 63)
fil.pack(side = TOP)
sub = Label(frame, text = "Select the options", font = ("Times bold", 8))
sub.pack()
checkframe = Frame(frame)
checkframe.pack()
apply_cat = BooleanVar()
categorycheck = Checkbutton(checkframe, text = "Category", font = f, variable = apply_cat, command = showchecks)
categorycheck.pack()
checkframe2 = Frame(checkframe)
checkt = Checkbutton(
    checkframe2, text = "Tops", font = f, variable = valt
)
checkt.pack(side = LEFT, padx = 5)
checks = Checkbutton(
    checkframe2, text = "Skirts", font = f, variable = vals
)
checks.pack(side = LEFT, padx = 5)
checkd = Checkbutton(
    checkframe2, text = "Dresses", font = f, variable = vald
)
checkd.pack(side = LEFT, padx = 5)
checkh = Checkbutton(
    checkframe2, text = "Headbands", font = f, variable = valh
)
checkh.pack(side = LEFT, padx = 5)
checkb = Checkbutton(
    checkframe2, text = "Bags", font = f, variable = valb
)
checkb.pack(side = LEFT, padx = 5)

frame2 = Frame(frame)
frame2.pack()
apply_quant = BooleanVar()
quantitycheck = Checkbutton(frame2, text = "Quantity", variable = apply_quant, font = f, command = showchecks)
quantitycheck.pack()
quantityframe = Frame(frame2)
label_quant = Label(quantityframe, text = "Quantity", font = f)
label_quant.pack(padx = 5, side = LEFT)
quant_num = IntVar()
quantity = Entry(quantityframe, textvariable = quant_num, font = f)
quantity.pack(side = LEFT)

frame3 = Frame(frame)
frame3.pack()
apply_price = BooleanVar()
pricecheck = Checkbutton(frame3, text = "Price", variable = apply_price, font = f, command = showchecks)
pricecheck.pack()
priceframe = Frame(frame3)
label_price = Label(priceframe, text = "Price", font = f)
label_price.pack(padx = 5, side = LEFT)
price_num = DoubleVar()
price = Entry(priceframe, textvariable = price_num, font = f)
price.pack(side = LEFT)

buttonframe = Frame(frame)
buttonframe.pack()
button = Button(buttonframe, text = "Apply", command = apply, background = "white", font = f, width = 10)
button.pack(pady = 5)

framedb = Frame(ws)
framedb.grid()
trv = ttk.Treeview(framedb, columns = (1, 2, 3, 4), show = "headings", height = 18)
trv.pack()
trv.heading(1, text = "ID", anchor = "center")
trv.heading(2, text = "Category", anchor = "center")
trv.heading(3, text = "Quantity", anchor = "center")
trv.heading(4, text = "Price", anchor = "center")
trv.column('#1', anchor = "center", width = 140, stretch = FALSE)
trv.column('#2', anchor = "center", width = 140, stretch = FALSE)
trv.column('#3', anchor = "center", width = 140, stretch = FALSE)
trv.column('#4', anchor = "center", width = 140, stretch = FALSE)

i = IntVar()
i.set(1) 
def getdata(doc_ref, filter):
    for doc in doc_ref:
        x = doc.to_dict()
        if len(x)!=0:
            if(filter):            
                if(apply_quant.get() and apply_price.get()):
                    if(x['Quantity'] == quant_num.get() and x['Price'] == price_num.get()):
                        trv.insert('', END, iid = i.get(), values = (x["id"], x["Category"], x["Quantity"], x["Price"]))
                elif(apply_quant.get()):
                    if(x['Quantity'] == quant_num.get()):
                        trv.insert('', END, iid = i.get(), values = (x["id"], x["Category"], x["Quantity"], x["Price"]))
                elif(apply_price.get()):
                    if(x['Price'] == price_num.get()):
                        trv.insert('', END, iid = i.get(), values = (x["id"], x["Category"], x["Quantity"], x["Price"]))
                else:
                    trv.insert('', i.get(), values = (x["id"], x["Category"], x["Quantity"], x["Price"]))
            else:
                trv.insert('', i.get(), values = (x["id"], x["Category"], x["Quantity"], x["Price"]))
            i.set(i.get()+1)

def getproducts(tops, skirts, dresses, headbands, bags, filter):
    if(filter):
        if(tops == False and skirts == False and dresses == False and headbands == False and bags == False):
            getproducts(True, True, True, True, True, True)
        else:
            if(tops):
                tops_ref = db.collection('tops').stream()
                getdata(tops_ref, filter)
            if(skirts):
                skirts_ref = db.collection('skirts').stream()
                getdata(skirts_ref, filter)
            if(dresses):
                dresses_ref = db.collection('dresses').stream()
                getdata(dresses_ref, filter)
            if(headbands):
                headbands_ref = db.collection('headbands').stream()
                getdata(headbands_ref, filter)
            if(bags):
                bags_ref = db.collection('bags').stream()
                getdata(bags_ref, filter)
    else:
        if(tops):
            tops_ref = db.collection('tops').stream()
            getdata(tops_ref, filter)
        if(skirts):
            skirts_ref = db.collection('skirts').stream()
            getdata(skirts_ref, filter)
        if(dresses):
            dresses_ref = db.collection('dresses').stream()
            getdata(dresses_ref, filter)
        if(headbands):
            headbands_ref = db.collection('headbands').stream()
            getdata(headbands_ref, filter)
        if(bags):
            bags_ref = db.collection('bags').stream()
            getdata(bags_ref, filter)

def dell():
    for i in trv.get_children():
        trv.delete(i)

productid = StringVar()
productCategory = StringVar()
productQuantity = IntVar()
productPrice = DoubleVar()
def item_selected(event):
    for selected_item in trv.selection():
        item = trv.item(selected_item)
        record = item['values']
        productid.set(record[0])
        productCategory.set(record[1])
        productQuantity.set(record[2])
        productPrice.set(record[3])

trv.bind('<<TreeviewSelect>>', item_selected)

#add
addframe = Frame(ws)
addframe.grid()
add_l = Label(addframe, text = "Add", font = t, anchor = "center", width = 40)
add_l.pack(side = TOP)
subadd = Label(addframe, text = "Add a new product", font = ("Times bold", 8))
subadd.pack()
labid = Label(addframe, text = "Id:", font = f, anchor = "w")
labid.pack(fill = "both", padx = 5)
entryaddid = StringVar()
enid = Entry(addframe, textvariable = entryaddid, font = f)
enid.pack(fill = "both", padx = 5, pady = 10)
addctg = Label(addframe, text = "Category:", font = f, anchor = "w")
addctg.pack(fill = "both", padx = 5)

addcategory = StringVar()
addcategory.set("tops") # default value
opt = OptionMenu(addframe, addcategory, "skirts", "dresses", "headbands", "bags")
opt.pack(fill = "both", padx = 5)
opt.configure(background = "white", font = f)
labprice = Label(addframe, text = "Price:", font = f, anchor = "w")
labprice.pack(fill = "both", padx = 5)
priceadd = DoubleVar()
enprice = Entry(addframe, textvariable = priceadd, font = f)
enprice.pack(fill = "both", padx = 5, pady = 10)
labquant = Label(addframe, text = "Quantity:", font = f, anchor = "w")
labquant.pack(fill = "both", padx = 5)
entryaddquant = IntVar()
enedquant = Entry(addframe, textvariable = entryaddquant, font = f)
enedquant.pack(fill = "both", padx = 5, pady = 10)

def addfunction():
    if(entryaddid.get() == ""):
        messagebox.showerror("Error", "Product ID missing")
    else:
        try:
            if(db.collection(addcategory.get()).document(entryaddid.get()).get().exists):
                messagebox.showerror("Error", "Product already exists")
            else:
                dell()
                db.collection(addcategory.get()).document(entryaddid.get()).set({'id': entryaddid.get(), 'Category': addcategory.get(), 'Price': priceadd.get(), 'Quantity': entryaddquant.get()})
                addcategory.set("tops")
                entryaddid.set("")
                priceadd.set(0.00)
                entryaddquant.set(0)
                index()
        except:
            messagebox.showerror("Error", "Invalid values")
   
   
addbutton = Button(addframe, text = "Done", command = addfunction, anchor = "center", width = 20, background = "white", font = f)
addbutton.pack(side = LEFT, padx = 5)

#edit
editframe = Frame(ws)
editframe.grid()
edit_l = Label(editframe, text = "Edit", font = t, width = 40)
edit_l.pack(side = TOP)
subedit = Label(editframe, text = "Edit a product", font = ("Times bold", 8))
subedit.pack()
editframe2 = Frame(editframe)
editframe2.pack()
labid2 = Label(editframe2, text = "Id", font = f, anchor = "w", width = 15, background = "white", relief = "ridge", padx = 10)
labid2.pack(side = LEFT, padx = 5, pady = 5)
enedid = Entry(editframe2, textvariable = productid, font = f, state = DISABLED)
enedid.pack(side = LEFT, padx = 5)
editframe3 = Frame(editframe)
editframe3.pack()
labcat = Label(editframe3, text = "Category", font = f,  anchor = "w", width = 15, background = "white", relief = "ridge", padx = 10)
labcat.pack(side = LEFT, padx = 5, pady = 5)
enedcat = Entry(editframe3, textvariable = productCategory, font = f, state = DISABLED)
enedcat.pack(side = LEFT, padx = 5)
editframe4 = Frame(editframe)
editframe4.pack()
labprice2 = Label(editframe4, text = "Price", font = f,  anchor = "w", width = 15, background = "white", relief = "ridge", padx = 10)
labprice2.pack(side = LEFT, padx = 5, pady = 5)
enedprice = Entry(editframe4, textvariable = productPrice, font = f)
enedprice.pack(side = LEFT, padx = 5)
editframe5 = Frame(editframe)
editframe5.pack()
labquant2 = Label(editframe5, text = "Quantity", font = f,  anchor = "w", width = 15, background = "white", relief = "ridge", padx = 10)
labquant2.pack(side = LEFT, padx = 5, pady = 5)
enedquant = Entry(editframe5, textvariable = productQuantity, font = f)
enedquant.pack(side = LEFT, padx = 5)

def editfunction():
    try:
        dell()
        db.collection(productCategory.get()).document(productid.get()).set({'id': productid.get(), 'Category': productCategory.get(), 'Price': productPrice.get(), 'Quantity': productQuantity.get()})
        index() #reload
    except:
         messagebox.showerror("Error", "Invalid values")

editbutton = Button(editframe, text = "Edit", command = editfunction, font = f, anchor = "center", background = "white", width = 20)
editbutton.pack(side = LEFT, padx = 5, pady = 5)

def add():
    addframe.grid()
    frame.grid_forget()
    framedb.grid_forget()
    bottomindex.grid_forget()
    editframe.grid_forget()

def edit():
    editframe.grid()
    frame.grid_forget()
    framedb.grid_forget()
    bottomindex.grid_forget()
    addframe.grid_forget()

#index bottom buttons
bottomindex = Frame(ws)
bottomindex.grid()

def deletefunction():
    db.collection(productCategory.get()).document(productid.get()).delete()
    dell()
    index() #reload

def reset():
    python = sys.executable
    os.execl(python, python, * sys.argv)

newbutton = Button(bottomindex, text = "Add", command = add, font = f, background = "white", anchor = "center", width = 15)
newbutton.pack(side = LEFT, padx = 5)
modbutton = Button(bottomindex, text = "Edit", command = edit, font = f, background = "white", anchor = "center", width = 15)
modbutton.pack(side = LEFT, padx = 5)
resetbutton = Button(bottomindex, text = "Reset", command = reset, font = f, background = "white", anchor = "center", width = 15)
resetbutton.pack(side = LEFT, padx = 5)
delbutton = Button(bottomindex, text = "Delete", command = deletefunction, font = f, background = "#ff3333", anchor = "center", width = 15)
delbutton.pack(side = LEFT, padx = 5)

def index():
    frame.grid()
    framedb.grid()
    bottomindex.grid()
    addframe.grid_forget()
    editframe.grid_forget()
    
    #get all products
    getproducts(TRUE, TRUE, TRUE, TRUE, TRUE, FALSE)

def back():
    frame.grid()
    framedb.grid()
    bottomindex.grid()
    addframe.grid_forget()
    editframe.grid_forget()

backadd = Button(addframe, text = "Back", command = back, anchor = "center", width = 20, background = "white", font = f)
backadd.pack(side = LEFT, padx = 5)
backedit = Button(editframe, text = "Back", command = back, anchor = "center", width = 20, background = "white", font = f)
backedit.pack(side = LEFT, padx = 5)

index()
ws.mainloop()