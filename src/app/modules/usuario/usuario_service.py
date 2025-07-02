from nest.core import Injectable
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.shared.database.models.usuario import Usuario
from .dto.usuario_dto import UsuarioCreate, UsuarioCreateResponse
from datetime import datetime


@Injectable()
class UsuarioService:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, password: str, hash_password: str) -> bool:
        return self.pwd_context.verify(password, hash_password)

    def create_user(self, db: Session, usuario: UsuarioCreate):
        try:
            usuario_db = Usuario(
                email=usuario.email,
                username=usuario.username,
                password=self.hash_password(usuario.password),
                nome=usuario.nome,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
            db.add(usuario_db)
            db.commit()
            db.refresh(usuario_db)
            return UsuarioCreateResponse.model_validate(usuario_db)
        except Exception as e:
            db.rollback()
            raise e

    def get_user_by_email(self, db: Session, email: str):
        return db.query(Usuario).filter(Usuario.email == email).first()

    def get_user_by_username(self, db: Session, username: str):
        return db.query(Usuario).filter(Usuario.username == username).first()

    def change_password(self, db: Session, user_email: str, new_password: str):
        try:
            user = self.get_user_by_email(db, user_email)
            if not user:
                raise Exception("Usuario nao encontrado")
            setattr(user, "password", self.hash_password(new_password))
            setattr(user, "updated_at", datetime.now())
            db.commit()
            db.refresh(user)
            return user
        except Exception as e:
            db.rollback()
            raise e
