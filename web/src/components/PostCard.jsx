import dayjs from 'dayjs';
import PropTypes from 'prop-types';

const attachmentShape = PropTypes.shape({
  id: PropTypes.number.isRequired,
  attachment: PropTypes.string.isRequired,
  type: PropTypes.string.isRequired
});

function Attachment({ attachment }) {
  if (attachment.type === 'image') {
    return <img className="post-card__media" src={attachment.url || attachment.attachment} alt="Зображення допису" loading="lazy" />;
  }

  if (attachment.type === 'video') {
    return (
      <video className="post-card__media" controls>
        <source src={attachment.url || attachment.attachment} />
        Ваш браузер не підтримує відео тег.
      </video>
    );
  }

  return null;
}

Attachment.propTypes = {
  attachment: attachmentShape.isRequired
};

export default function PostCard({ post, locale }) {
  const createdAt = dayjs(post.pub_date).locale(locale).fromNow();
  const avatar = post.member?.avatar_url;

  return (
    <article className="post-card">
      <header className="post-card__header">
        {avatar ? (
          <img className="post-card__avatar" src={avatar} alt={post.member?.username ?? 'Аватар'} loading="lazy" />
        ) : (
          <div className="post-card__avatar placeholder" aria-hidden />
        )}
        <div>
          <p className="post-card__author">{post.member?.username}</p>
          <time className="post-card__date" dateTime={post.pub_date}>{createdAt}</time>
        </div>
      </header>
      <h2 className="post-card__title">{post.title}</h2>
      {post.content && <p className="post-card__content">{post.content}</p>}
      {post.attachments?.length > 0 && (
        <div className="post-card__attachments">
          {post.attachments.map((attachment) => (
            <Attachment key={attachment.id} attachment={attachment} />
          ))}
        </div>
      )}
    </article>
  );
}

PostCard.propTypes = {
  post: PropTypes.shape({
    id: PropTypes.number.isRequired,
    title: PropTypes.string,
    content: PropTypes.string,
    pub_date: PropTypes.string.isRequired,
    attachments: PropTypes.arrayOf(attachmentShape),
    member: PropTypes.shape({
      username: PropTypes.string,
      avatar_url: PropTypes.string
    })
  }).isRequired,
  locale: PropTypes.object.isRequired
};
