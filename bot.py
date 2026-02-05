# Import library discord.py
import discord
from discord.ext import commands

# Import DB manager (logic database) dan config
from logic import DB_Manager
from config import DATABASE, TOKEN

# Mengatur intent (izin event yang bisa diterima bot)
intents = discord.Intents.default()
intents.messages = True  # Mengizinkan bot membaca pesan

# Membuat bot dengan prefix "!" dan intent yang sudah diatur
bot = commands.Bot(command_prefix='!', intents=intents)

# Inisialisasi database manager
manager = DB_Manager(DATABASE)

# Event yang dijalankan saat bot berhasil online
@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user}')

# Command !start
@bot.command(name='start')
async def start_command(ctx):
    # Mengirim pesan sambutan
    await ctx.send(
        "Halo! Saya adalah bot manajer proyek\n"
        "Saya akan membantu kamu menyimpan proyek dan informasi tentangnya!)"
    )
    # Menampilkan daftar command
    await info(ctx)

# Command !info → menampilkan semua perintah bot
@bot.command(name='info')
async def info(ctx):
    await ctx.send("""
Berikut adalah perintah yang dapat membantu kamu:

!new_project - gunakan untuk menambahkan proyek baru
!projects - gunakan untuk menampilkan semua proyek
!update_projects - gunakan untuk mengubah data proyek
!skills - gunakan untuk menghubungkan keterampilan ke proyek
!delete - gunakan untuk menghapus proyek

Kamu juga dapat memasukkan nama proyek untuk mengetahui informasi tentangnya!
""")

# Command !new_project → menambah proyek baru
@bot.command(name='new_project')
async def new_project(ctx):
    await ctx.send("Masukkan nama proyek:")

    # Fungsi check agar bot hanya membaca pesan dari user & channel yang sama
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    # Menunggu input nama proyek
    name = await bot.wait_for('message', check=check)

    # Menyimpan data awal (user_id, nama proyek)
    data = [ctx.author.id, name.content]

    # Meminta link proyek
    await ctx.send("Masukkan link proyek")
    link = await bot.wait_for('message', check=check)
    data.append(link.content)

    # Mengambil daftar status dari database
    statuses = [x[0] for x in manager.get_statuses()]
    await ctx.send("Masukkan status proyek saat ini", delete_after=60.0)
    await ctx.send("\n".join(statuses), delete_after=60.0)

    # Menunggu input status
    status = await bot.wait_for('message', check=check)

    # Validasi status
    if status.content not in statuses:
        await ctx.send(
            "Kamu memilih status yang tidak ada dalam daftar, silakan coba lagi!)",
            delete_after=60.0
        )
        return

    # Mengambil status_id berdasarkan nama status
    status_id = manager.get_status_id(status.content)
    data.append(status_id)

    # Menyimpan proyek ke database
    manager.insert_project([tuple(data)])
    await ctx.send("Proyek telah disimpan")

# Command !projects → menampilkan semua proyek user
@bot.command(name='projects')
async def get_projects(ctx):
    user_id = ctx.author.id
    projects = manager.get_projects(user_id)

    if projects:
        # Menyusun teks daftar proyek
        text = "\n".join(
            [f"Project name: {x[2]} \nLink: {x[4]}\n" for x in projects]
        )
        await ctx.send(text)
    else:
        await ctx.send(
            'Kamu belum memiliki proyek!\n'
            'Kamu dapat menambahkannya menggunakan perintah !new_project'
        )

# Command !skills → menambahkan skill ke proyek
@bot.command(name='skills')
async def skills(ctx):
    user_id = ctx.author.id
    projects = manager.get_projects(user_id)

    if projects:
        # Ambil nama proyek saja
        projects = [x[2] for x in projects]
        await ctx.send('Pilih proyek yang ingin kamu tambahkan keterampilan')
        await ctx.send("\n".join(projects))

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        # Input nama proyek
        project_name = await bot.wait_for('message', check=check)

        # Validasi proyek
        if project_name.content not in projects:
            await ctx.send(
                'Kamu tidak memiliki proyek tersebut, silakan coba lagi!)'
            )
            return

        # Ambil daftar skill dari database
        skills = [x[1] for x in manager.get_skills()]
        await ctx.send('Pilih keterampilan')
        await ctx.send("\n".join(skills))

        # Input skill
        skill = await bot.wait_for('message', check=check)

        # Validasi skill
        if skill.content not in skills:
            await ctx.send(
                'Sepertinya kamu memilih keterampilan yang tidak ada dalam daftar!'
            )
            return

        # Simpan skill ke proyek
        manager.insert_skill(user_id, project_name.content, skill.content)
        await ctx.send(
            f'Keterampilan {skill.content} telah ditambahkan ke proyek {project_name.content}'
        )
    else:
        await ctx.send(
            'Kamu belum memiliki proyek!\n'
            'Kamu dapat menambahkannya menggunakan perintah !new_project'
        )

# Command !delete → menghapus proyek
@bot.command(name='delete')
async def delete_project(ctx):
    user_id = ctx.author.id
    projects = manager.get_projects(user_id)

    if projects:
        projects = [x[2] for x in projects]
        await ctx.send("Pilih proyek yang ingin kamu hapus")
        await ctx.send("\n".join(projects))

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        project_name = await bot.wait_for('message', check=check)

        if project_name.content not in projects:
            await ctx.send('Kamu tidak memiliki proyek tersebut, silakan coba lagi!')
            return

        # Ambil project_id lalu hapus
        project_id = manager.get_project_id(project_name.content, user_id)
        manager.delete_project(user_id, project_id)

        await ctx.send(f'Proyek {project_name.content} telah dihapus!')
    else:
        await ctx.send(
            'Kamu belum memiliki proyek!\n'
            'Kamu dapat menambahkannya menggunakan perintah !new_project'
        )

# Command !update_projects → mengubah data proyek
@bot.command(name='update_projects')
async def update_projects(ctx):
    user_id = ctx.author.id
    projects = manager.get_projects(user_id)

    if projects:
        projects = [x[2] for x in projects]
        await ctx.send("Pilih proyek yang ingin kamu ubah")
        await ctx.send("\n".join(projects))

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        project_name = await bot.wait_for('message', check=check)

        if project_name.content not in projects:
            await ctx.send("Ada yang salah! Silakan pilih proyek lagi:")
            return

        # Pilihan atribut yang bisa diubah
        attributes = {
            'Nama proyek': 'project_name',
            'Deskripsi': 'description',
            'Link': 'url',
            'Status': 'status_id'
        }

        await ctx.send("Pilih apa yang ingin kamu ubah")
        await ctx.send("\n".join(attributes.keys()))

        attribute = await bot.wait_for('message', check=check)

        if attribute.content not in attributes:
            await ctx.send("Pilihan tidak valid!")
            return

        # Jika update status → ambil status_id
        if attribute.content == 'Status':
            statuses = manager.get_statuses()
            await ctx.send("Pilih status baru")
            await ctx.send("\n".join([x[0] for x in statuses]))

            update_info = await bot.wait_for('message', check=check)

            if update_info.content not in [x[0] for x in statuses]:
                await ctx.send("Status tidak valid!")
                return

            update_info = manager.get_status_id(update_info.content)
        else:
            await ctx.send(f"Masukkan nilai baru untuk {attribute.content}")
            update_info = await bot.wait_for('message', check=check)
            update_info = update_info.content

        # Update data di database
        manager.update_projects(
            attributes[attribute.content],
            (update_info, project_name.content, user_id)
        )

        await ctx.send("Selesai! Pembaruan telah dilakukan!")
    else:
        await ctx.send(
            'Kamu belum memiliki proyek!\n'
            'Kamu dapat menambahkannya menggunakan perintah !new_project'
        )

# Menjalankan bot
bot.run(TOKEN)
