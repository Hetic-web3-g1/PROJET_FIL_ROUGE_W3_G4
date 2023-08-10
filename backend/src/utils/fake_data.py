import random
import datetime
from uuid import UUID

from faker import Faker
from sqlalchemy import func, select

from ..entities.academies.models import academy_table
from ..entities.academies.schemas import AcademyCreate
from ..entities.academies.service import create_academy
from ..entities.comments.models import comment_table
from ..entities.comments.schemas import CommentCreate
from ..entities.comments.service import create_comment
from ..entities.biographies.models import biography_table
from ..entities.biographies.schemas import BiographyCreate
from ..entities.biographies.service import create_biography
from ..entities.masterclasses.models import masterclass_table, masterclass_user_table
from ..entities.masterclasses.schemas import MasterclassCreate, MasterclassUserCreate
from ..entities.masterclasses.service import (
    create_masterclass,
    assign_user_to_masterclass,
)
from ..entities.users.models import user_table
from ..entities.users.schemas import UserCreate, User
from ..entities.users.service import create_user
from ..entities.work_analyses.models import work_analysis_table
from ..entities.work_analyses.schemas import WorkAnalysisCreate
from ..entities.work_analyses.service import create_work_analysis
from ..database import service as db_service
from ..database.db_engine import engine


status = ["created", "in-progress", "completed", "archived", "in-review", "rejected"]
primary_role = ["user", "admin"]
secondary_role = ["manager", "writer", "video_editor", "traductor"]
instruments = [
    "other",
    "piano",
    "violin",
    "celio",
    "voice",
    "viola",
    "clarinet",
    "flute",
    "oboe",
    "chamber music",
    "trombone",
]

user = User(
    id=UUID("12345648-1234-1234-1234-123456789123"),
    first_name="admin",
    last_name="admin",
    email="admin@gmail.com",
    primary_role="admin",
    secondary_role=["manager", "video_editor", "traductor", "writer"],
    academy_id=UUID("12345648-1234-1234-1234-123456789123"),
    image_id=None,
    created_by=None,
    created_at=datetime.datetime.now(),
    updated_at=datetime.datetime.now(),
    updated_by=None,
)


def create_fixed_academy_fake():
    with engine.begin() as conn:
        academy = AcademyCreate(**{"name": "Saline Royale Academy"})
        return db_service.create_object(
            conn,
            academy_table,
            academy.dict(),
            object_id="12345648-1234-1234-1234-123456789123",
        )


def create_fixed_user_fake():
    with engine.begin() as conn:
        fixed_user = UserCreate(
            **{
                "first_name": "admin",
                "last_name": "admin",
                "email": "admin@admin.com",
                "primary_role": "admin",
                "secondary_role": ["manager", "video_editor", "traductor", "writer"],
                "academy_id": UUID("12345648-1234-1234-1234-123456789123"),
            }
        )
        return db_service.create_object(
            conn,
            user_table,
            fixed_user.dict(),
            object_id="12345648-1234-1234-1234-123456789123",
            user_id=user.id,
        )


def create_fixed_masterclass_fake():
    with engine.begin() as conn:
        masterclass = MasterclassCreate(
            **{
                "academy_id": UUID("12345648-1234-1234-1234-123456789123"),
                "title": "Fake Masterclass",
                "description": "Description of fake masterclass",
                "instrument": [random.choice(instruments) for _ in range(2, 4)],
                "status": random.choice(status),
            }
        )
        return db_service.create_object(
            conn,
            masterclass_table,
            masterclass.dict(),
            object_id="12345648-1234-1234-1234-123456789123",
            user_id=user.id,
        )


def assign_user_to_masterclass_fake():
    with engine.begin() as conn:
        masterclass_user = MasterclassUserCreate(
            **{
                "user_id": UUID("12345648-1234-1234-1234-123456789123"),
                "masterclass_id": UUID("12345648-1234-1234-1234-123456789123"),
                "masterclass_role": random.choice(secondary_role),
            }
        )
        assign_user_to_masterclass(conn, masterclass_user)


####################


def create_academy_fake():
    with engine.begin() as conn:
        academy = AcademyCreate(**{"name": Faker().company()})
        create_academy(conn, academy)


def create_user_fake():
    with engine.begin() as conn:
        first_name = Faker().first_name()
        last_name = Faker().last_name()
        new_user = UserCreate(
            **{
                "first_name": first_name,
                "last_name": last_name,
                "email": first_name + "." + last_name + "@gmail.com",
                "primary_role": random.choice(primary_role),
                "secondary_role": [
                    random.choice(secondary_role) for _ in range(random.randint(1, 2))
                ],
                "academy_id": UUID("12345648-1234-1234-1234-123456789123"),
            }
        )
        create_user(conn, new_user, user)


def create_masterclass_fake():
    with engine.begin() as conn:
        masterclass = MasterclassCreate(
            **{
                "academy_id": UUID("12345648-1234-1234-1234-123456789123"),
                "title": random.choice(compositions_title),
                "description": random.choice(compositions_description),
                "instrument": [random.choice(instruments) for _ in range(2, 4)],
                "status": random.choice(status),
            }
        )
        create_masterclass(conn, masterclass, user)


####################


def create_biography_fake():
    with engine.begin() as conn:
        type = ["teacher", "compositor"]
        biography = BiographyCreate(
            **{
                "first_name": Faker().first_name(),
                "last_name": Faker().last_name(),
                "instrument": [
                    random.choice(instruments) for _ in range(random.randint(1, 3))
                ],
                "nationality": Faker().country(),
                "website": Faker().url(),
                "award": [random.choice(awards) for _ in range(random.randint(2, 5))],
                "content": random.choice(biography_content),
                "type": random.choice(type),
                "status": random.choice(status),
            }
        )
        create_biography(conn, biography, user)


def create_work_analyse_fake():
    with engine.begin() as conn:
        work_analysis = WorkAnalysisCreate(
            **{
                "title": random.choice(compositions_title),
                "about": random.choice(compositions_description),
                "learning": [
                    random.choice(learnings) for _ in range(random.randint(2, 5))
                ],
                "content": random.choice(compositions_description),
                "status": random.choice(status),
            }
        )
        create_work_analysis(conn, work_analysis, user)


####################


def create_comment_fake():
    with engine.begin() as conn:
        comment = CommentCreate(**{"content": random.choice(comments)})
        create_comment(conn, comment, user)


####################


def has_data(conn, table):
    result = conn.execute(select(func.count()).select_from(table)).scalar()
    return result > 0


def generate_data():
    tables = {
        academy_table: create_academy_fake,
        user_table: create_user_fake,
        biography_table: create_biography_fake,
        comment_table: create_comment_fake,
        masterclass_table: create_masterclass_fake,
        masterclass_user_table: assign_user_to_masterclass_fake,
        work_analysis_table: create_work_analyse_fake,
    }
    with engine.begin() as conn:
        for table, create_func in tables.items():
            if not has_data(conn, table):  # Check if table is empty
                if table == academy_table:
                    create_fixed_academy_fake()
                if table == user_table:
                    create_fixed_user_fake()
                if table == masterclass_table:
                    create_fixed_masterclass_fake()
                for _ in range(10):
                    create_func()


########## Data ##########

compositions_title = [
    "Brahms - Clarinet Sonata No. 2 in E-flat Major, Op. 120 (2nd movement)",
    "Schumann - Three Romances for Oboe and Piano, Op. 94",
    "Mendelssohn - Clarinet Sonata in E-flat Major",
    "Schubert - Arpeggione Sonata in A Minor, D. 821 (2nd movement)",
    "Mozart - Clarinet Quintet in A Major, K. 581 (2nd movement)",
    "Beethoven - Violin Sonata No. 5 in F Major, Op. 24 'Spring' (1st movement)",
    "Weber - Clarinet Concerto No. 1 in F Minor, Op. 73 (2nd movement)",
    "Debussy - Première Rhapsodie for Clarinet and Piano",
    "Fauré - Clarinet Sonata No. 1 in D Minor, Op. 120",
    "Poulenc - Sonata for Clarinet and Piano (1st movement)",
    "Saint-Saëns - Sonata for Clarinet and Piano in E-flat Major, Op. 167",
    "Bruch - Eight Pieces for Clarinet, Viola, and Piano, Op. 83",
    "Ravel - Introduction and Allegro for Harp, Flute, Clarinet, and String Quartet",
    "Dvorák - Bagatelles for Two Violins, Cello, and Harmonium, Op. 47",
    "Françaix - Tema con variazioni for Clarinet and Piano",
    "Glinka - Trio Pathétique in D Minor for Clarinet, Bassoon, and Piano",
    "Brahms - Violin Sonata No. 1 in G Major, Op. 78 (2nd movement)",
    "Schumann - Fantasiestücke for Clarinet and Piano, Op. 73",
    "Reger - Sonata in F-sharp Minor for Clarinet and Piano, Op. 49 No. 2",
    "Hindemith - Sonata for Clarinet and Piano",
]


compositions_description = [
    "Brahms - Clarinet Sonata No. 2 in E-flat Major, Op. 120 (2nd movement) - Graceful clarinet melodies within an introspective movement.",
    "Schumann - Three Romances for Oboe and Piano, Op. 94 - Heartfelt oboe miniatures capturing various emotional moods.",
    "Mendelssohn - Clarinet Sonata in E-flat Major - Delightful and charming dialogues between clarinet and piano.",
    "Schubert - Arpeggione Sonata in A Minor, D. 821 (2nd movement) - Melancholic arpeggione and expressive melodies.",
    "Mozart - Clarinet Quintet in A Major, K. 581 (2nd movement) - Serene clarinet melody against a chamber ensemble backdrop.",
    "Beethoven - Violin Sonata No. 5 in F Major, Op. 24 'Spring' (1st movement) - Lively and cheerful violin-piano interplay with spring-like themes.",
    "Weber - Clarinet Concerto No. 1 in F Minor, Op. 73 (2nd movement) - Lyrical clarinet showcasing against an orchestral tapestry.",
    "Debussy - Première Rhapsodie for Clarinet and Piano - Dreamy clarinet passages weaving through impressionistic textures.",
    "Fauré - Clarinet Sonata No. 1 in D Minor, Op. 120 - Lyrical and heartfelt clarinet-piano collaboration.",
    "Poulenc - Sonata for Clarinet and Piano (1st movement) - Playful and spirited clarinet and piano dialogue.",
    "Saint-Saëns - Sonata for Clarinet and Piano in E-flat Major, Op. 167 - Charming piece highlighting clarinet's agility and lyricism.",
    "Bruch - Eight Pieces for Clarinet, Viola, and Piano, Op. 83 - Character pieces showcasing clarinet and viola individually and in duet.",
    "Ravel - Introduction and Allegro for Harp, Flute, Clarinet, and String Quartet - Dynamic ensemble piece with harp, flute, clarinet, and strings.",
    "Dvorák - Bagatelles for Two Violins, Cello, and Harmonium, Op. 47 - Short melodious pieces with folk influences.",
    "Françaix - Tema con variazioni for Clarinet and Piano - Witty and inventive variations highlighting clarinet's character.",
    "Glinka - Trio Pathétique in D Minor for Clarinet, Bassoon, and Piano - Passionate trio with rich harmonies and virtuosic clarinet-bassoon passages.",
    "Brahms - Violin Sonata No. 1 in G Major, Op. 78 (2nd movement) - Serene violin-piano conversation in a tender movement.",
    "Schumann - Fantasiestücke for Clarinet and Piano, Op. 73 - Whimsical character pieces exploring different emotions.",
    "Reger - Sonata in F-sharp Minor for Clarinet and Piano, Op. 49 No. 2 - Expressive and introspective clarinet-piano work.",
    "Hindemith - Sonata for Clarinet and Piano - Neoclassical composition blending traditional and modern elements.",
]


awards = [
    "Awarded the prestigious Avery Fisher Career Grant for exceptional violin performance.",
    "Renowned cellist and winner of the Tchaikovsky Competition's top prize.",
    "Pioneering conductor known for innovative interpretations of symphonic classics.",
    "Leading soprano acclaimed for her interpretations of Wagnerian roles.",
    "Eminent pianist who received the Chopin International Piano Competition's gold medal.",
    "Esteemed composer of symphonies and operas, recipient of a Pulitzer Prize.",
    "Highly regarded flutist recognized for blending traditional and contemporary sounds.",
    "Gifted violinist and laureate of the Menuhin Competition's first prize.",
    "Distinguished conductor hailed for rejuvenating orchestras and fostering new talent.",
    "Renowned mezzo-soprano with Grammy-winning recordings of Baroque arias.",
    "Visionary composer known for blending electronic elements with orchestral music.",
    "Celebrated pianist acclaimed for virtuosic renditions of Romantic repertoire.",
    "Versatile clarinetist who has premiered numerous contemporary works.",
    "Accomplished violist and advocate for modern chamber music compositions.",
    "Eminent musicologist honored for groundbreaking research in Baroque-era manuscripts.",
    "Noted conductor of film scores, recognized for bringing cinematic music to life.",
    "Acclaimed countertenor with interpretations of Handel's operatic arias.",
    "Leading harpist known for revitalizing the instrument's solo and chamber music repertoire.",
    "Exceptional trumpeter awarded top prizes in international brass competitions.",
    "Esteemed music educator recognized for pioneering interactive music education programs.",
]


biography_content = [
    "Clara Schumann (1819–1896): A prominent 19th-century pianist and composer, Clara Schumann was a trailblazer who defied societal norms to pursue her musical passions. Her virtuosic piano performances captivated audiences across Europe. As a composer, she contributed exquisite pieces marked by emotional depth and intricate structures, leaving a lasting mark on the Romantic era.",
    "Franz Liszt (1811–1886): Renowned for his extraordinary pianism and charismatic presence, Franz Liszt transcended conventional musical boundaries. A key figure of the Romantic movement, his compositions, such as the virtuosic 'Transcendental Études' and the symphonic poem 'Les Préludes,' showcased his innovative style and artistic innovation.",
    "Antonín Dvořák (1841–1904): Hailing from Bohemia, Antonín Dvořák fused folk melodies with classical forms, infusing his works with a distinct national identity. His symphonies, chamber music, and operas, like the powerful 'New World Symphony' and the lyrically enchanting 'Rusalka,' illustrate his ability to evoke profound emotions through his compositions.",
    "Maria Callas (1923–1977): An iconic soprano renowned for her dramatic intensity and vocal versatility, Maria Callas brought operatic characters to life with unmatched emotional depth. Her performances in works like 'Carmen' and 'Norma' showcased her ability to connect with audiences on a visceral level, earning her a place among the greatest opera singers in history.",
    "Igor Stravinsky (1882–1971): A transformative composer, Igor Stravinsky's revolutionary compositions, including 'The Rite of Spring,' challenged musical conventions and redefined modernism. His ability to traverse diverse styles, from neoclassicism to serialism, left an indelible mark on 20th-century music.",
    "Pyotr Ilyich Tchaikovsky (1840–1893): A Russian composer whose works resonate with emotional richness, Tchaikovsky's symphonies, ballets, and operas, such as 'Swan Lake' and the impassioned 'Pathétique Symphony,' reflect his ability to express profound feelings through music, captivating audiences worldwide.",
    "Leonard Bernstein (1918–1990): A versatile musician, Leonard Bernstein was not only a gifted conductor but also a prolific composer and educator. His compositions, including the Broadway classic 'West Side Story' and his symphonic works, embody his ability to blend classical and popular influences.",
    "Antonio Vivaldi (1678–1741): The Baroque mastermind behind the beloved 'Four Seasons,' Antonio Vivaldi's virtuosic violin concertos and sacred choral compositions showcased his vibrant melodies and inventive use of orchestration, leaving an indelible mark on the Baroque era.",
    "Édith Piaf (1915–1963): A legendary French chanteuse, Édith Piaf's emotive interpretations of chansons captured the essence of life's joys and sorrows. Her powerful voice and charismatic presence transformed her into a global sensation and an enduring cultural icon.",
    "Johann Sebastian Bach (1685–1750): A towering figure in classical music history, Johann Sebastian Bach's intricate counterpoint, as displayed in works like the 'Mass in B Minor' and 'Art of Fugue,' has profoundly influenced generations of composers. His ability to craft music of both intellectual depth and emotional resonance defines his enduring legacy.",
    "Ludwig van Beethoven (1770–1827): A visionary composer who bridged the Classical and Romantic eras, Beethoven's revolutionary works, such as the transformative Ninth Symphony and the 'Moonlight Sonata,' reflect his artistic evolution and indomitable spirit.",
    "Wolfgang Amadeus Mozart (1756–1791): A child prodigy whose musical genius blossomed into a prolific career, Mozart's operas, symphonies, and chamber works, like the beloved 'Eine kleine Nachtmusik,' remain beloved for their melodic beauty and emotional depth.",
    "Gustav Mahler (1860–1911): A late-Romantic composer and conductor, Gustav Mahler's symphonies, such as the monumental 'Symphony No. 2' (Resurrection Symphony), grapple with profound existential themes, showcasing his ability to evoke deep emotions through orchestral composition.",
    "Maria Anna Mozart (1751–1829): The elder sister of Wolfgang Amadeus Mozart, Maria Anna Mozart was a talented keyboardist and composer in her own right. Her compositions offer insights into the musical environment of the time and her own artistic contributions.",
    "Giuseppe Verdi (1813–1901): The Italian master of opera, Giuseppe Verdi's grand operas, including 'La Traviata,' 'Aida,' and 'Rigoletto,' are characterized by captivating melodies, vivid characters, and powerful storytelling that continues to captivate audiences worldwide.",
    "Hildegard von Bingen (1098–1179): An accomplished composer, philosopher, and mystic of the medieval period, Hildegard von Bingen's sacred chants and visionary writings have left an indelible mark on both music and spirituality.",
    "Franz Schubert (1797–1828): An Austrian composer known for his lieder and chamber music, Franz Schubert's compositions, such as 'Trout Quintet' and the song cycle 'Winterreise,' capture his ability to convey deep emotions through melody.",
    "Benjamin Britten (1913–1976): A British composer celebrated for his operatic works, orchestral compositions, and vocal music, Benjamin Britten's pieces, like the operas 'Peter Grimes' and 'Billy Budd,' showcase his distinctive voice and mastery of dramatic storytelling.",
    "Camille Saint-Saëns (1835–1921): A French composer with a wide-ranging oeuvre, Camille Saint-Saëns' compositions, including the enchanting 'Carnival of the Animals' and the dynamic symphonies, exemplify his compositional versatility and rich musical language.",
    "Henryk Wieniawski (1835–1880): A virtuoso Polish violinist and composer, Henryk Wieniawski's demanding violin compositions, such as the dazzling 'Polonaise Brillante,' continue to challenge and inspire violinists with their technical brilliance and lyrical beauty.",
]


learnings = [
    "Developing and following a trajectory.",
    "Playing expressively.",
    "Diction and articulation.",
    "Maintaining good posture.",
    "Intonation.",
    "Understanding musical phrasing.",
    "Effective use of dynamics.",
    "Mastering various bowing techniques.",
    "Balancing melody and accompaniment.",
    "Rhythmic precision.",
    "Interpreting different musical styles.",
    "Collaborating with other musicians.",
    "Breath control (for wind and vocal performers).",
    "Improving finger dexterity and coordination.",
    "Navigating complex rhythms.",
    "Translating emotion into sound.",
    "Developing a distinctive tone.",
    "Memorization techniques.",
    "Adapting to different performance venues.",
    "Effective communication through music.",
]


comments = [
    "The seamless integration of visuals and music creates an engaging narrative that truly resonates.",
    "The way you've synchronized the biographical details with the music enhances the emotional impact.",
    "Kudos for selecting a background score that complements the subject's musical journey so harmoniously.",
    "The pacing and transitions in the video biography mirror the artist's life story brilliantly.",
    "The use of carefully chosen music snippets adds depth and authenticity to the biography.",
    "While the music choice is fitting, consider adjusting the volume levels for a smoother listening experience.",
    "There's a slight timing mismatch between the visuals and the music; syncing them precisely will enhance the video's professionalism.",
    "In this section, the biography's text overlaps with the crescendo of the music, affecting readability.",
    "Be mindful of the video's audio quality—it's crucial for delivering the biography and music clearly.",
    "The abrupt ending of the music track leaves the audience wanting a smoother conclusion; consider a more gradual fade-out.",
    "The balance between the artist's spoken words and the accompanying music is well-executed.",
    "The video captures the artist's passion for music and their journey in a compelling way.",
    "The choice to incorporate performance footage adds a dynamic layer to the biography.",
    "The music's emotional resonance effectively amplifies the artist's personal anecdotes.",
    "Consider refining the video's color grading to match the mood set by the music.",
    "The biography's pacing aligns beautifully with the ebb and flow of the music.",
    "The captions that complement the music's lyrics enhance the viewer's understanding of the artist's story.",
    "The video's ending, with a subtle instrumental fade-out, provides a satisfying closure.",
    "The narrative's seamless progression makes the viewer feel immersed in the artist's musical journey.",
    "A minor typo in the biography's text at 1:35 needs correction for a polished presentation.",
]
