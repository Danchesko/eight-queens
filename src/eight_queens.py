from time import time
from tkinter import ttk, messagebox, Canvas, TOP, StringVar, Spinbox, Tk, E, W
from itertools import permutations

class EightQueens():

    def __init__(self, master):
        self.n = 8
        self.queens = (0 for i in range(self.n)) 
        self.solution_index = 0
        self.solutions = [] 

        # build gui
        self.master = master
        self.master.title('Eight Queens')
        self.master.configure(background='#c6b5a5')
        self.master.minsize(400, 450)
        self.master.resizable(True, True)
        self.master.bind('<Configure>', lambda e: self._draw_board())

        self.style = ttk.Style()
        self.style.configure('TFrame', background='#c6b5a5')
        self.style.configure('TButton', background='#c6b5a5')
        self.style.configure('TLabel', background='#c6b5a5')

        self.board_canvas = Canvas(self.master)
        self.board_canvas.pack()

        self.controls_frame = ttk.Frame(self.master)
        self.controls_frame.pack(side=TOP, pady=10)

        ttk.Label(self.controls_frame, text='Number of Queens:',
                  font='Helvetica 10 bold').grid(row=0, column=0)
        self.n_var = StringVar()
        self.n_var.set(self.n)
        Spinbox(self.controls_frame, from_=4, to=99, width=2,
                font='Helvetica 10 bold', textvariable=self.n_var).grid(row=0, column=1)
        ttk.Button(self.controls_frame, text = 'Get Next Solution',
                   command=self._solution_callback).grid(row=1, column=0, columnspan=2)
        ttk.Label(self.controls_frame).grid(row=0, column=2, padx=10)

        self.solution_var = StringVar()
        self.time_var = StringVar()
        self.solution_var.set('--')
        self.time_var.set('--')
        ttk.Label(self.controls_frame, text='Solution:',
                  font='Helvetica 10 bold').grid(row=0, column=3, sticky=(E))
        ttk.Label(self.controls_frame, textvariable=self.solution_var,
                  font='Helvetica 10').grid(row=0, column=4, sticky=(W))
        ttk.Label(self.controls_frame, text='Elapsed Time:',
                  font='Helvetica 10 bold').grid(row=1, column=3, sticky=(E))
        ttk.Label(self.controls_frame, textvariable = self.time_var,
                  font='Helvetica 10').grid(row=1, column=4, sticky=(W))

        self._solution_callback()

    def _draw_board(self):
        maxboardsize = min(self.master.winfo_width(), self.master.winfo_height() - 70)
        cellsize = maxboardsize // self.n
        self.board_canvas.config(height=self.n*cellsize, width=self.n*cellsize)
        self.board_canvas.delete('all')

        for i in range(self.n):
            for j in range(self.n):
                if (i+j+self.n) % 2: 
                    self.board_canvas.create_rectangle(i*cellsize, j*cellsize,
                                                       i*cellsize+cellsize, j*cellsize+cellsize,
                                                       fill='#993526')
            # draw a queen
            self.board_canvas.create_text(i*cellsize+cellsize//2, self.queens[i]*cellsize+cellsize//2,
                                          text=u'\u265B', font=('Arial', cellsize//2), fill='#212121')

    def _solution_callback(self):
        try:
            input_val = int(self.n_var.get())
        except:
            messagebox.showerror(title='Invalid Input',
                                 message='Must enter a number of queens')
            return

        if self.n != input_val or self.solutions == []:
            if 4 > input_val:
                messagebox.showerror(title='Invalid Value for number of queen ',
                                     message='Number of queens must be greater than 4.')
            else:
                self.n = input_val
                self.solution_index = 0
                self.solutions = []
                start_time = time()

                columns = range(self.n)
                for perm in permutations(columns):
                    diag1 = set()
                    diag2 = set()
                    for i in columns:
                        diag1.add(perm[i]+i)
                        diag2.add(perm[i]-i)
                    if self.n == len(diag1) == len(diag2):
                        self.solutions.append(perm)

                elapsed_time = time() - start_time
                self.time_var.set('{0:.3f}s'.format(elapsed_time))
        else:
            self.solution_index += 1

        self.queens = self.solutions[self.solution_index % len(self.solutions)]
        self.solution_var.set('{0}/{1}'.format(self.solution_index % len(self.solutions) + 1, len(self.solutions)))
        self._draw_board()

def main():
    root = Tk()
    gui = EightQueens(root)
    root.mainloop()


if __name__ == "__main__":
    main()
